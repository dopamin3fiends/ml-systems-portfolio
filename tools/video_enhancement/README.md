# 🎬 Video Enhancement Suite v1.0

Professional video processing queue manager with multi-backend support, priority scheduling, and concurrent processing.

## Features

### 🚀 Multi-Backend Support
- **Topaz Video AI** - Professional upscaling and enhancement
- **FFmpeg** - Universal video processing and conversion
- **HandBrake** - High-quality encoding
- **Automatic Fallback** - Intelligently selects best available backend

### ⚡ Advanced Queue Management
- **Priority Scheduling** - Process critical jobs first (LOW/MEDIUM/HIGH/CRITICAL)
- **Concurrent Processing** - Run multiple jobs simultaneously
- **Automatic Retry** - Failed jobs retry up to 3 times
- **Persistent Storage** - Queue survives restarts
- **Real-time Monitoring** - Track job status and progress

### 🎯 Built-in Presets
- `upscale_2x` / `upscale_4x` - Increase resolution
- `denoise` - Remove video noise
- `sharpen` - Enhance detail
- `compress` - Reduce file size

## Quick Start

### Installation

**FFmpeg (Recommended):**
```bash
# Windows (Chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

**Optional Backends:**
- Topaz Video AI: https://www.topazlabs.com/video-ai
- HandBrake: https://handbrake.fr/downloads.php

### Usage

**Add jobs to queue:**
```bash
python cli.py add input.mp4 output_4k.mp4 --preset upscale_4x --priority high
python cli.py add noisy.mp4 clean.mp4 --preset denoise --priority medium
```

**Start processing:**
```bash
python cli.py process --workers 2
```

**Monitor queue:**
```bash
python cli.py list
python cli.py stats
```

**Run demo:**
```bash
python cli.py demo
```

## Output Files

All jobs are tracked in `data/tmp/video_queue.json`:
```json
{
  "jobs": {
    "abc-123": {
      "job_id": "abc-123",
      "input_file": "input.mp4",
      "output_file": "output_4k.mp4",
      "preset": "upscale_4x",
      "status": "completed",
      "priority": 3,
      "backend": "ffmpeg",
      "processing_time": 45.2
    }
  }
}
```

## Integration with Orchestrator

The Video Enhancement Suite integrates seamlessly with the Legacy Systems Orchestrator:

### Via REST API:
```bash
curl -X POST http://localhost:8000/run/tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "video_enhancement",
    "input_text": "input.mp4|output_4k.mp4|upscale_4x|high"
  }'
```

### Via Dashboard:
1. Navigate to http://localhost:8000
2. Select "Video Enhancement Suite"
3. Provide: `input.mp4|output_4k.mp4|upscale_4x|high`
4. Click "Run Tool"

## Architecture

```
video_enhancement/
├── models.py          # Data classes (VideoJob, JobStatus, Priority, Backend)
├── processor.py       # Multi-backend video processor with fallback
├── queue_manager.py   # Priority queue with concurrent workers
├── cli.py            # Command-line interface
└── README.md         # This file
```

## Advanced Features

### Custom Presets
Edit `processor.py` to add custom FFmpeg presets:
```python
preset_map = {
    "my_preset": ["-vf", "custom_filter", "-c:v", "libx264", "-crf", "18"],
}
```

### Concurrent Workers
Adjust worker count based on CPU/GPU capacity:
```bash
python cli.py process --workers 4  # 4 concurrent jobs
```

### Priority Override
Override automatic priority for urgent jobs:
```bash
python cli.py add video.mp4 output.mp4 --preset upscale_4x --priority critical
```

## Use Cases

### Content Creation
- Upscale footage to 4K/8K
- Denoise low-light video
- Compress for web delivery

### Video Forensics
- Enhance surveillance footage
- Sharpen blurry evidence
- Standardize formats for analysis

### Media Production
- Batch process raw footage
- Apply consistent enhancement
- Prepare multi-format deliverables

### Archival/Restoration
- Upscale old content
- Remove noise and artifacts
- Modernize legacy video

## Educational Use

This tool is designed for **legal video processing workflows** including:
- Personal media enhancement
- Professional content creation
- Forensic video analysis (with proper authorization)
- Educational research

**DO NOT use for:**
- Processing copyrighted content without permission
- Creating misleading or deceptive media
- Unauthorized surveillance footage enhancement

## License

MIT License - See LICENSE file for details

## Support

For issues, feature requests, or questions:
- GitHub: https://github.com/dopamin3fiends/ml-systems-portfolio
- Email: support@example.com

---

**Built with ❤️ by the Legacy Systems Team**
