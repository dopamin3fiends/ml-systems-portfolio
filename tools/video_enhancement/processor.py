"""
Video Enhancement Suite - Video Processor
Handles multi-backend video processing with fallback support
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional
import time

try:
    from models import Backend, ProcessingResult
except ImportError:
    from .models import Backend, ProcessingResult


class VideoProcessor:
    """
    Multi-backend video processor with automatic fallback
    
    Supports:
    - Topaz Video AI (professional upscaling/enhancement)
    - FFmpeg (universal video processing)
    - HandBrake (encoding/conversion)
    """
    
    def __init__(self):
        """Initialize processor and detect available backends"""
        self.available_backends = self._detect_backends()
    
    def _detect_backends(self) -> dict:
        """Detect which video processing backends are installed"""
        backends = {}
        
        # Check for Topaz Video AI
        if shutil.which("topaz-cli") or shutil.which("tvai"):
            backends[Backend.TOPAZ] = True
        
        # Check for FFmpeg
        if shutil.which("ffmpeg"):
            backends[Backend.FFMPEG] = True
        
        # Check for HandBrake
        if shutil.which("handbrakecli") or shutil.which("HandBrakeCLI"):
            backends[Backend.HANDBRAKE] = True
        
        return backends
    
    def select_backend(self, requested: Backend, preset: str) -> Optional[Backend]:
        """
        Select best available backend
        
        Args:
            requested: User-requested backend
            preset: Processing preset name
            
        Returns:
            Selected backend or None if none available
        """
        if requested == Backend.AUTO:
            # Prioritize based on preset
            if "upscale" in preset.lower() or "enhance" in preset.lower():
                if Backend.TOPAZ in self.available_backends:
                    return Backend.TOPAZ
            
            # Fallback order: Topaz > FFmpeg > HandBrake
            for backend in [Backend.TOPAZ, Backend.FFMPEG, Backend.HANDBRAKE]:
                if backend in self.available_backends:
                    return backend
            return None
        
        # Check if requested backend is available
        if requested in self.available_backends:
            return requested
        
        # Fallback to any available backend
        for backend in self.available_backends:
            return backend
        
        return None
    
    def process_video(
        self,
        job_id: str,
        input_file: str,
        output_file: str,
        preset: str,
        backend: Backend = Backend.AUTO
    ) -> ProcessingResult:
        """
        Process video file with specified backend
        
        Args:
            job_id: Unique job identifier
            input_file: Input video path
            output_file: Output video path
            preset: Processing preset
            backend: Requested backend
            
        Returns:
            ProcessingResult with success status and details
        """
        start_time = time.time()
        
        # Select backend
        selected_backend = self.select_backend(backend, preset)
        
        if not selected_backend:
            return ProcessingResult(
                success=False,
                job_id=job_id,
                error_message="No video processing backend available. Install FFmpeg, Topaz Video AI, or HandBrake."
            )
        
        # Process with selected backend
        try:
            if selected_backend == Backend.TOPAZ:
                result = self._process_topaz(input_file, output_file, preset)
            elif selected_backend == Backend.FFMPEG:
                result = self._process_ffmpeg(input_file, output_file, preset)
            elif selected_backend == Backend.HANDBRAKE:
                result = self._process_handbrake(input_file, output_file, preset)
            else:
                result = False
            
            processing_time = time.time() - start_time
            
            if result:
                return ProcessingResult(
                    success=True,
                    job_id=job_id,
                    output_file=output_file,
                    processing_time=processing_time,
                    backend_used=selected_backend
                )
            else:
                return ProcessingResult(
                    success=False,
                    job_id=job_id,
                    error_message=f"Processing failed with {selected_backend.value}",
                    processing_time=processing_time,
                    backend_used=selected_backend
                )
        
        except Exception as e:
            processing_time = time.time() - start_time
            return ProcessingResult(
                success=False,
                job_id=job_id,
                error_message=str(e),
                processing_time=processing_time,
                backend_used=selected_backend
            )
    
    def _process_topaz(self, input_file: str, output_file: str, preset: str) -> bool:
        """Process video with Topaz Video AI"""
        cmd = [
            "topaz-cli" if shutil.which("topaz-cli") else "tvai",
            "--input", input_file,
            "--output", output_file,
            "--preset", preset
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def _process_ffmpeg(self, input_file: str, output_file: str, preset: str) -> bool:
        """Process video with FFmpeg"""
        # Map preset to FFmpeg parameters
        preset_map = {
            "upscale_2x": ["-vf", "scale=iw*2:ih*2:flags=lanczos", "-c:v", "libx264", "-crf", "18"],
            "upscale_4x": ["-vf", "scale=iw*4:ih*4:flags=lanczos", "-c:v", "libx264", "-crf", "18"],
            "denoise": ["-vf", "hqdn3d=4:3:6:4.5", "-c:v", "libx264", "-crf", "18"],
            "sharpen": ["-vf", "unsharp=5:5:1.0:5:5:0.0", "-c:v", "libx264", "-crf", "18"],
            "compress": ["-c:v", "libx264", "-crf", "23", "-preset", "medium"],
            "default": ["-c:v", "libx264", "-crf", "18", "-preset", "medium"]
        }
        
        params = preset_map.get(preset, preset_map["default"])
        
        cmd = ["ffmpeg", "-i", input_file] + params + ["-y", output_file]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def _process_handbrake(self, input_file: str, output_file: str, preset: str) -> bool:
        """Process video with HandBrake"""
        handbrake_cmd = "handbrakecli" if shutil.which("handbrakecli") else "HandBrakeCLI"
        
        cmd = [
            handbrake_cmd,
            "-i", input_file,
            "-o", output_file,
            "--preset", preset if preset in ["Fast", "Normal", "HQ"] else "Normal"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def get_available_backends_info(self) -> dict:
        """Get information about available backends"""
        return {
            "topaz": Backend.TOPAZ in self.available_backends,
            "ffmpeg": Backend.FFMPEG in self.available_backends,
            "handbrake": Backend.HANDBRAKE in self.available_backends,
            "count": len(self.available_backends)
        }
