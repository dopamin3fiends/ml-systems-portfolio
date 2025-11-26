"""
Windows Feature Manager - Feature Management
PowerShell-based Windows optional feature management with safety checks
"""

import subprocess
import json
import uuid
import platform
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

try:
    from models import (
        WindowsFeature, FeatureState, OperationResult, OperationType,
        SystemBackup, FeatureCategory, FEATURE_METADATA
    )
except ImportError:
    from .models import (
        WindowsFeature, FeatureState, OperationResult, OperationType,
        SystemBackup, FeatureCategory, FEATURE_METADATA
    )


class WindowsFeatureManager:
    """
    Manages Windows optional features via PowerShell
    
    Features:
    - Query installed features
    - Enable/disable features with validation
    - Backup and restore feature states
    - Dependency checking
    - Admin privilege validation
    """
    
    def __init__(self):
        """Initialize feature manager"""
        self.is_windows = platform.system() == "Windows"
        self.backup_dir = Path("data/tmp/feature_backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _run_powershell(self, command: str) -> tuple[bool, str, str]:
        """
        Execute PowerShell command
        
        Args:
            command: PowerShell command to execute
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        if not self.is_windows:
            return False, "", "Not running on Windows"
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def is_admin(self) -> bool:
        """Check if running with administrator privileges"""
        if not self.is_windows:
            return False
        
        command = "([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"
        success, stdout, _ = self._run_powershell(command)
        
        return success and stdout.strip().lower() == "true"
    
    def list_features(self, state_filter: Optional[FeatureState] = None) -> List[WindowsFeature]:
        """
        List all Windows optional features
        
        Args:
            state_filter: Filter by feature state (None = all features)
            
        Returns:
            List of WindowsFeature objects
        """
        if not self.is_windows:
            return []
        
        # Query features using DISM
        command = "Get-WindowsOptionalFeature -Online | Select-Object FeatureName, State | ConvertTo-Json"
        success, stdout, stderr = self._run_powershell(command)
        
        if not success:
            return []
        
        try:
            # Parse JSON output
            if not stdout.strip():
                return []
            
            # Handle both single object and array
            data = json.loads(stdout)
            if not isinstance(data, list):
                data = [data]
            
            features = []
            for item in data:
                feature_name = item.get("FeatureName", "")
                state_str = item.get("State", "").lower()
                
                # Map state
                if "enabled" in state_str:
                    state = FeatureState.ENABLED
                elif "disabled" in state_str:
                    state = FeatureState.DISABLED
                else:
                    state = FeatureState.UNKNOWN
                
                # Apply filter
                if state_filter and state != state_filter:
                    continue
                
                # Get metadata if available
                metadata = FEATURE_METADATA.get(feature_name, {})
                category = metadata.get("category", FeatureCategory.UNKNOWN)
                description = metadata.get("description")
                restart_required = metadata.get("restart_required", False)
                
                feature = WindowsFeature(
                    name=feature_name,
                    display_name=feature_name.replace("-", " ").title(),
                    state=state,
                    category=category,
                    description=description,
                    restart_required=restart_required
                )
                
                features.append(feature)
            
            return features
        
        except json.JSONDecodeError:
            return []
    
    def get_feature(self, feature_name: str) -> Optional[WindowsFeature]:
        """
        Get specific feature details
        
        Args:
            feature_name: Name of the feature
            
        Returns:
            WindowsFeature or None if not found
        """
        features = self.list_features()
        
        for feature in features:
            if feature.name.lower() == feature_name.lower():
                return feature
        
        return None
    
    def enable_feature(self, feature_name: str, no_restart: bool = True) -> OperationResult:
        """
        Enable Windows optional feature
        
        Args:
            feature_name: Name of feature to enable
            no_restart: Suppress automatic restart
            
        Returns:
            OperationResult
        """
        if not self.is_windows:
            return OperationResult(
                success=False,
                operation=OperationType.ENABLE,
                feature_name=feature_name,
                message="Not running on Windows",
                error="Platform not supported"
            )
        
        if not self.is_admin():
            return OperationResult(
                success=False,
                operation=OperationType.ENABLE,
                feature_name=feature_name,
                message="Administrator privileges required",
                error="Not running as administrator"
            )
        
        # Build command
        restart_flag = "-NoRestart" if no_restart else ""
        command = f"Enable-WindowsOptionalFeature -Online -FeatureName '{feature_name}' {restart_flag} -All -ErrorAction Stop"
        
        success, stdout, stderr = self._run_powershell(command)
        
        if success:
            # Check if restart required
            restart_required = "restart" in stdout.lower() or "reboot" in stdout.lower()
            
            return OperationResult(
                success=True,
                operation=OperationType.ENABLE,
                feature_name=feature_name,
                message=f"Successfully enabled {feature_name}",
                restart_required=restart_required
            )
        else:
            return OperationResult(
                success=False,
                operation=OperationType.ENABLE,
                feature_name=feature_name,
                message=f"Failed to enable {feature_name}",
                error=stderr or "Unknown error"
            )
    
    def disable_feature(self, feature_name: str, no_restart: bool = True) -> OperationResult:
        """
        Disable Windows optional feature
        
        Args:
            feature_name: Name of feature to disable
            no_restart: Suppress automatic restart
            
        Returns:
            OperationResult
        """
        if not self.is_windows:
            return OperationResult(
                success=False,
                operation=OperationType.DISABLE,
                feature_name=feature_name,
                message="Not running on Windows",
                error="Platform not supported"
            )
        
        if not self.is_admin():
            return OperationResult(
                success=False,
                operation=OperationType.DISABLE,
                feature_name=feature_name,
                message="Administrator privileges required",
                error="Not running as administrator"
            )
        
        restart_flag = "-NoRestart" if no_restart else ""
        command = f"Disable-WindowsOptionalFeature -Online -FeatureName '{feature_name}' {restart_flag} -ErrorAction Stop"
        
        success, stdout, stderr = self._run_powershell(command)
        
        if success:
            restart_required = "restart" in stdout.lower() or "reboot" in stdout.lower()
            
            return OperationResult(
                success=True,
                operation=OperationType.DISABLE,
                feature_name=feature_name,
                message=f"Successfully disabled {feature_name}",
                restart_required=restart_required
            )
        else:
            return OperationResult(
                success=False,
                operation=OperationType.DISABLE,
                feature_name=feature_name,
                message=f"Failed to disable {feature_name}",
                error=stderr or "Unknown error"
            )
    
    def backup_features(self) -> SystemBackup:
        """
        Create backup of current feature states
        
        Returns:
            SystemBackup object
        """
        features = self.list_features()
        feature_states = {f.name: f.state for f in features}
        
        # Get system info
        hostname = platform.node()
        os_version = platform.version()
        
        backup = SystemBackup(
            backup_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            features=feature_states,
            hostname=hostname,
            os_version=os_version
        )
        
        # Save backup to file
        backup_file = self.backup_dir / f"backup_{backup.backup_id}.json"
        with open(backup_file, 'w') as f:
            json.dump(backup.to_dict(), f, indent=2)
        
        return backup
    
    def restore_features(self, backup_id: str, dry_run: bool = False) -> List[OperationResult]:
        """
        Restore features from backup
        
        Args:
            backup_id: Backup identifier
            dry_run: If True, only show what would be changed
            
        Returns:
            List of OperationResult objects
        """
        # Load backup
        backup_file = self.backup_dir / f"backup_{backup_id}.json"
        
        if not backup_file.exists():
            return [OperationResult(
                success=False,
                operation=OperationType.RESTORE,
                feature_name="",
                message="Backup not found",
                error=f"No backup with ID {backup_id}"
            )]
        
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        backup = SystemBackup.from_dict(backup_data)
        
        # Get current features
        current_features = {f.name: f.state for f in self.list_features()}
        
        results = []
        
        # Compare and restore differences
        for feature_name, target_state in backup.features.items():
            current_state = current_features.get(feature_name, FeatureState.UNKNOWN)
            
            if current_state == target_state:
                continue  # No change needed
            
            if dry_run:
                results.append(OperationResult(
                    success=True,
                    operation=OperationType.RESTORE,
                    feature_name=feature_name,
                    message=f"Would change {feature_name}: {current_state.value} → {target_state.value}"
                ))
            else:
                # Perform restore
                if target_state == FeatureState.ENABLED:
                    result = self.enable_feature(feature_name)
                elif target_state == FeatureState.DISABLED:
                    result = self.disable_feature(feature_name)
                else:
                    continue
                
                results.append(result)
        
        return results
    
    def get_system_info(self) -> dict:
        """Get Windows system information"""
        return {
            "platform": platform.system(),
            "version": platform.version(),
            "hostname": platform.node(),
            "is_admin": self.is_admin(),
            "is_windows": self.is_windows
        }
