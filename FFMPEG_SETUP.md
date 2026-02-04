# FFmpeg Setup Guide for VS Code

## What is FFmpeg?
FFmpeg is a powerful multimedia framework for handling audio and video files. It's required by many Python libraries like `pydub`, `moviepy`, and others for audio/video processing.

## Installation Steps

### Option 1: Using Chocolatey (Recommended)
1. Open PowerShell as Administrator
2. Install Chocolatey if not already installed:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
3. Install FFmpeg:
   ```powershell
   choco install ffmpeg
   ```

### Option 2: Manual Installation
1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add to PATH:
   - Open System Properties → Environment Variables
   - Edit `Path` variable
   - Add `C:\ffmpeg\bin`
   - Click OK

### Option 3: Using Scoop
```powershell
scoop install ffmpeg
```

## Verify Installation
```powershell
ffmpeg -version
```

## VS Code Configuration

### 1. Update settings.json
Add FFmpeg path to VS Code settings (if needed):

**File → Preferences → Settings → Open Settings (JSON)**

```json
{
    "terminal.integrated.env.windows": {
        "PATH": "${env:PATH};C:\\ffmpeg\\bin"
    }
}
```

### 2. Workspace Settings
Create `.vscode/settings.json` in your project:

```json
{
    "terminal.integrated.env.windows": {
        "FFMPEG_BINARY": "ffmpeg",
        "FFPROBE_BINARY": "ffprobe"
    }
}
```

## Python Integration

### For pydub
```python
from pydub import AudioSegment
from pydub.playback import play

# pydub will automatically find ffmpeg if it's in PATH
audio = AudioSegment.from_mp3("audio.mp3")
```

### For moviepy
```python
from moviepy.editor import VideoFileClip

# moviepy will use ffmpeg from PATH
video = VideoFileClip("video.mp4")
```

## Troubleshooting

### Issue: "ffmpeg not found"
**Solution:**
1. Restart VS Code after installation
2. Check PATH:
   ```powershell
   $env:PATH -split ';' | Select-String ffmpeg
   ```
3. Verify ffmpeg location:
   ```powershell
   (Get-Command ffmpeg).Source
   ```

### Issue: Permission denied
**Solution:**
- Run PowerShell as Administrator
- Check execution policy:
  ```powershell
  Get-ExecutionPolicy
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Issue: VS Code terminal doesn't recognize ffmpeg
**Solution:**
1. Restart VS Code completely
2. Or reload window: `Ctrl+Shift+P` → "Developer: Reload Window"
3. Create new terminal session

## Testing in VS Code

Run in VS Code terminal:
```powershell
# Check version
ffmpeg -version

# Check ffprobe
ffprobe -version

# Test with Python
python -c "import subprocess; print(subprocess.run(['ffmpeg', '-version'], capture_output=True).stdout.decode())"
```

## Common Use Cases

### Convert audio format
```powershell
ffmpeg -i input.wav output.mp3
```

### Extract audio from video
```powershell
ffmpeg -i video.mp4 -vn -acodec copy audio.mp3
```

### Compress audio
```powershell
ffmpeg -i input.mp3 -b:a 128k output.mp3
```

## Additional Resources
- FFmpeg Documentation: https://ffmpeg.org/documentation.html
- FFmpeg Windows Builds: https://www.gyan.dev/ffmpeg/builds/
- Chocolatey Package: https://community.chocolatey.org/packages/ffmpeg

---
**Last Updated:** January 22, 2026
