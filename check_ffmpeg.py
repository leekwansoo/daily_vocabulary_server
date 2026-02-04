"""
FFmpeg Configuration Checker
This script verifies that ffmpeg is properly configured in your environment.
"""

import subprocess
import sys
import os
from pathlib import Path


def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    print("=" * 60)
    print("FFmpeg Configuration Check")
    print("=" * 60)
    
    # Check if ffmpeg is in PATH
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ FFmpeg is installed and accessible")
            version_line = result.stdout.split('\n')[0]
            print(f"  Version: {version_line}")
        else:
            print("✗ FFmpeg found but returned an error")
            print(f"  Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg is NOT found in PATH")
        print("\nPlease install ffmpeg using one of these methods:")
        print("  1. choco install ffmpeg  (using Chocolatey)")
        print("  2. scoop install ffmpeg  (using Scoop)")
        print("  3. Manual installation - see FFMPEG_SETUP.md")
        return False
    except Exception as e:
        print(f"✗ Error checking ffmpeg: {e}")
        return False
    
    # Check ffprobe
    try:
        result = subprocess.run(
            ['ffprobe', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ FFprobe is installed and accessible")
        else:
            print("✗ FFprobe found but returned an error")
    except FileNotFoundError:
        print("⚠ FFprobe is NOT found (usually comes with ffmpeg)")
    except Exception as e:
        print(f"⚠ Error checking ffprobe: {e}")
    
    # Check PATH
    print("\n" + "=" * 60)
    print("PATH Information")
    print("=" * 60)
    
    path_env = os.environ.get('PATH', '')
    ffmpeg_paths = [p for p in path_env.split(';') if 'ffmpeg' in p.lower()]
    
    if ffmpeg_paths:
        print("FFmpeg-related paths found in PATH:")
        for p in ffmpeg_paths:
            print(f"  • {p}")
    else:
        print("No FFmpeg-related paths found in PATH")
    
    # Try to find ffmpeg location
    try:
        if sys.platform == 'win32':
            result = subprocess.run(
                ['where', 'ffmpeg'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("\nFFmpeg location(s):")
                for line in result.stdout.strip().split('\n'):
                    print(f"  • {line}")
        else:
            result = subprocess.run(
                ['which', 'ffmpeg'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"\nFFmpeg location: {result.stdout.strip()}")
    except Exception as e:
        print(f"\nCouldn't determine ffmpeg location: {e}")
    
    # Check environment variables
    print("\n" + "=" * 60)
    print("Environment Variables")
    print("=" * 60)
    
    ffmpeg_binary = os.environ.get('FFMPEG_BINARY')
    ffprobe_binary = os.environ.get('FFPROBE_BINARY')
    
    if ffmpeg_binary:
        print(f"FFMPEG_BINARY = {ffmpeg_binary}")
    else:
        print("FFMPEG_BINARY not set")
    
    if ffprobe_binary:
        print(f"FFPROBE_BINARY = {ffprobe_binary}")
    else:
        print("FFPROBE_BINARY not set")
    
    print("\n" + "=" * 60)
    print("Result: ✓ FFmpeg is properly configured!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = check_ffmpeg()
    sys.exit(0 if success else 1)
