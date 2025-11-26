"""
PathPulse - Pattern Analyzer
Detects suspicious file system activity patterns (ransomware, data exfiltration, etc.)
"""

import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter

try:
    from models import FileEvent, ThreatPattern, EventType, RiskLevel, FileCategory
except ImportError:
    from .models import FileEvent, ThreatPattern, EventType, RiskLevel, FileCategory


class PatternAnalyzer:
    """
    Analyzes file system events for suspicious patterns
    
    Detects:
    - Mass deletion (ransomware, data destruction)
    - Rapid encryption (ransomware)
    - Unusual access patterns (data exfiltration)
    - Privilege escalation (system file modification)
    - Suspicious executables (malware deployment)
    """
    
    def __init__(self):
        """Initialize pattern analyzer"""
        self.encryption_extensions = [
            ".encrypted", ".locked", ".crypto", ".crypt", ".enc",
            ".WNCRY", ".wcry", ".KEYH0LES", ".locky", ".cerber"
        ]
    
    def analyze_events(self, events: List[FileEvent], window_seconds: int = 300) -> List[ThreatPattern]:
        """
        Analyze events for threat patterns
        
        Args:
            events: List of FileEvent objects to analyze
            window_seconds: Time window for pattern detection (default 5 minutes)
            
        Returns:
            List of detected ThreatPattern objects
        """
        if not events:
            return []
        
        patterns = []
        
        # Only analyze recent events within the time window
        cutoff_time = datetime.now() - timedelta(seconds=window_seconds)
        recent_events = [e for e in events if e.timestamp >= cutoff_time]
        
        if not recent_events:
            return []
        
        # Detect various threat patterns
        patterns.extend(self._detect_mass_deletion(recent_events))
        patterns.extend(self._detect_ransomware_encryption(recent_events))
        patterns.extend(self._detect_rapid_file_creation(recent_events))
        patterns.extend(self._detect_system_file_tampering(recent_events))
        patterns.extend(self._detect_sensitive_access(recent_events))
        patterns.extend(self._detect_unusual_extensions(recent_events))
        
        return patterns
    
    def _detect_mass_deletion(self, events: List[FileEvent]) -> List[ThreatPattern]:
        """Detect mass file deletion (ransomware, sabotage)"""
        deletions = [e for e in events if e.event_type == EventType.DELETED]
        
        if len(deletions) < 10:  # Threshold: 10+ deletions
            return []
        
        # Calculate deletion rate
        if deletions:
            time_span = (deletions[-1].timestamp - deletions[0].timestamp).total_seconds()
            deletion_rate = len(deletions) / max(time_span, 1)
        else:
            return []
        
        # High risk if many deletions in short time
        risk_level = RiskLevel.CRITICAL if deletion_rate > 2 else RiskLevel.HIGH
        confidence = min(1.0, len(deletions) / 50)
        
        pattern = ThreatPattern(
            pattern_type="mass_deletion",
            description=f"Mass file deletion detected: {len(deletions)} files deleted in {time_span:.1f}s ({deletion_rate:.2f} files/sec)",
            events=deletions,
            risk_level=risk_level,
            confidence=confidence,
            first_seen=deletions[0].timestamp,
            last_seen=deletions[-1].timestamp,
            event_count=len(deletions),
            recommended_action="URGENT: Possible ransomware or data destruction. Isolate system, check backups, investigate deleted files."
        )
        
        return [pattern]
    
    def _detect_ransomware_encryption(self, events: List[FileEvent]) -> List[ThreatPattern]:
        """Detect rapid file encryption (ransomware)"""
        # Look for files with encryption extensions
        encrypted_files = []
        for event in events:
            if event.event_type in [EventType.CREATED, EventType.MODIFIED]:
                if any(event.path.lower().endswith(ext) for ext in self.encryption_extensions):
                    encrypted_files.append(event)
        
        if len(encrypted_files) < 5:  # Threshold: 5+ encrypted files
            return []
        
        time_span = (encrypted_files[-1].timestamp - encrypted_files[0].timestamp).total_seconds()
        encryption_rate = len(encrypted_files) / max(time_span, 1)
        
        pattern = ThreatPattern(
            pattern_type="ransomware_encryption",
            description=f"Ransomware encryption detected: {len(encrypted_files)} files encrypted in {time_span:.1f}s ({encryption_rate:.2f} files/sec)",
            events=encrypted_files,
            risk_level=RiskLevel.CRITICAL,
            confidence=0.95,
            first_seen=encrypted_files[0].timestamp,
            last_seen=encrypted_files[-1].timestamp,
            event_count=len(encrypted_files),
            recommended_action="CRITICAL: Ransomware attack detected. Immediately disconnect from network, do not reboot, contact incident response team."
        )
        
        return [pattern]
    
    def _detect_rapid_file_creation(self, events: List[FileEvent]) -> List[ThreatPattern]:
        """Detect rapid file creation (malware deployment, data staging)"""
        creations = [e for e in events if e.event_type == EventType.CREATED and not e.metadata.get("is_directory")]
        
        if len(creations) < 20:  # Threshold: 20+ files
            return []
        
        time_span = (creations[-1].timestamp - creations[0].timestamp).total_seconds()
        creation_rate = len(creations) / max(time_span, 1)
        
        # Check if files are executables
        exe_count = sum(1 for e in creations if e.file_category == FileCategory.EXECUTABLE)
        
        risk_level = RiskLevel.HIGH if exe_count > 5 else RiskLevel.MEDIUM
        confidence = min(1.0, len(creations) / 100)
        
        pattern = ThreatPattern(
            pattern_type="rapid_file_creation",
            description=f"Rapid file creation: {len(creations)} files created in {time_span:.1f}s ({exe_count} executables)",
            events=creations,
            risk_level=risk_level,
            confidence=confidence,
            first_seen=creations[0].timestamp,
            last_seen=creations[-1].timestamp,
            event_count=len(creations),
            recommended_action="Investigate process responsible for file creation. Check for malware deployment or data staging."
        )
        
        return [pattern]
    
    def _detect_system_file_tampering(self, events: List[FileEvent]) -> List[ThreatPattern]:
        """Detect system file modifications (privilege escalation, rootkit)"""
        system_events = [
            e for e in events
            if e.event_type in [EventType.MODIFIED, EventType.CREATED]
            and e.file_category == FileCategory.SYSTEM
        ]
        
        if not system_events:
            return []
        
        pattern = ThreatPattern(
            pattern_type="system_file_tampering",
            description=f"System file tampering: {len(system_events)} system files modified/created",
            events=system_events,
            risk_level=RiskLevel.HIGH,
            confidence=0.85,
            first_seen=system_events[0].timestamp,
            last_seen=system_events[-1].timestamp,
            event_count=len(system_events),
            recommended_action="Investigate system file modifications. Check for rootkit, privilege escalation, or unauthorized system changes."
        )
        
        return [pattern]
    
    def _detect_sensitive_access(self, events: List[FileEvent]) -> List[ThreatPattern]:
        """Detect sensitive file access (credential theft, data exfiltration)"""
        sensitive_events = [
            e for e in events
            if e.file_category == FileCategory.SENSITIVE or e.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        ]
        
        if len(sensitive_events) < 3:  # Threshold: 3+ sensitive files
            return []
        
        pattern = ThreatPattern(
            pattern_type="sensitive_file_access",
            description=f"Sensitive file access: {len(sensitive_events)} sensitive files accessed (credentials, keys, etc.)",
            events=sensitive_events,
            risk_level=RiskLevel.HIGH,
            confidence=0.75,
            first_seen=sensitive_events[0].timestamp,
            last_seen=sensitive_events[-1].timestamp,
            event_count=len(sensitive_events),
            recommended_action="Investigate access to sensitive files. Check for credential theft, key exfiltration, or unauthorized access."
        )
        
        return [pattern]
    
    def _detect_unusual_extensions(self, events: List[FileEvent]) -> List[ThreatPattern]:
        """Detect unusual file extensions (obfuscation, malware)"""
        unusual_extensions = [
            ".tmp.exe", ".jpg.exe", ".pdf.exe", ".scr", ".pif",
            ".vbs", ".wsf", ".hta", ".bat.exe"
        ]
        
        unusual_files = []
        for event in events:
            if event.event_type == EventType.CREATED:
                if any(event.path.lower().endswith(ext) for ext in unusual_extensions):
                    unusual_files.append(event)
        
        if not unusual_files:
            return []
        
        pattern = ThreatPattern(
            pattern_type="unusual_extensions",
            description=f"Unusual file extensions: {len(unusual_files)} files with suspicious extensions (obfuscation/malware)",
            events=unusual_files,
            risk_level=RiskLevel.MEDIUM,
            confidence=0.70,
            first_seen=unusual_files[0].timestamp,
            last_seen=unusual_files[-1].timestamp,
            event_count=len(unusual_files),
            recommended_action="Scan files with unusual extensions for malware. Check for obfuscated executables."
        )
        
        return [pattern]
    
    def generate_report(self, events: List[FileEvent], patterns: List[ThreatPattern]) -> dict:
        """
        Generate analysis report
        
        Args:
            events: All analyzed events
            patterns: Detected threat patterns
            
        Returns:
            Report dictionary
        """
        # Event statistics
        event_type_counts = Counter(e.event_type.value for e in events)
        risk_level_counts = Counter(e.risk_level.value for e in events)
        category_counts = Counter(e.file_category.value for e in events)
        
        # Pattern statistics
        pattern_type_counts = Counter(p.pattern_type for p in patterns)
        
        # Overall risk assessment
        if any(p.risk_level == RiskLevel.CRITICAL for p in patterns):
            overall_risk = RiskLevel.CRITICAL
        elif any(p.risk_level == RiskLevel.HIGH for p in patterns):
            overall_risk = RiskLevel.HIGH
        elif any(p.risk_level == RiskLevel.MEDIUM for p in patterns):
            overall_risk = RiskLevel.MEDIUM
        else:
            overall_risk = RiskLevel.LOW
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_events": len(events),
            "total_patterns": len(patterns),
            "overall_risk": overall_risk.value,
            "event_types": dict(event_type_counts),
            "risk_levels": dict(risk_level_counts),
            "file_categories": dict(category_counts),
            "detected_patterns": dict(pattern_type_counts),
            "patterns": [p.to_dict() for p in patterns]
        }
