# PowerShell Commands Reference Guide

## Windows System Tools & GUI Applications

### Task & System Management
```powershell
# Task Scheduler
taskschd.msc

# Task Manager
taskmgr

# System Configuration
msconfig

# System Information
msinfo32

# Services
services.msc

# Event Viewer
eventvwr.msc

# Performance Monitor
perfmon.msc

# Resource Monitor
resmon

# Registry Editor
regedit

# Group Policy Editor (Pro/Enterprise only)
gpedit.msc
```

### Control Panel & Settings
```powershell
# Control Panel
control

# System Properties
sysdm.cpl

# Programs and Features
appwiz.cpl

# Network Connections
ncpa.cpl

# User Accounts
netplwiz

# Sound Settings
mmsys.cpl

# Power Options
powercfg.cpl

# Device Manager
devmgmt.msc

# Disk Management
diskmgmt.msc

# Computer Management
compmgmt.msc

# Windows Settings (Modern UI)
start ms-settings:
```

---

## File & Directory Operations

### Navigation
```powershell
# Get current directory
Get-Location
# or
pwd

# Change directory
Set-Location C:\Users
# or
cd C:\Users

# List files and folders
Get-ChildItem
# or
ls
# or
dir

# List with details
Get-ChildItem | Format-Table Name, Length, LastWriteTime

# List only files
Get-ChildItem -File

# List only directories
Get-ChildItem -Directory

# Recursive listing
Get-ChildItem -Recurse

# Search for files
Get-ChildItem -Path C:\ -Filter *.txt -Recurse -ErrorAction SilentlyContinue
```

### File Operations
```powershell
# Create directory
New-Item -ItemType Directory -Path "C:\NewFolder"
# or
mkdir C:\NewFolder

# Create file
New-Item -ItemType File -Path "C:\file.txt"

# Copy file
Copy-Item -Path "source.txt" -Destination "destination.txt"

# Copy directory recursively
Copy-Item -Path "C:\Source" -Destination "C:\Dest" -Recurse

# Move file
Move-Item -Path "source.txt" -Destination "C:\destination.txt"

# Rename file
Rename-Item -Path "oldname.txt" -NewName "newname.txt"

# Delete file
Remove-Item -Path "file.txt"

# Delete directory recursively
Remove-Item -Path "C:\Folder" -Recurse -Force

# Read file content
Get-Content -Path "file.txt"

# Write to file (overwrite)
"Hello World" | Out-File -FilePath "file.txt"

# Append to file
"New Line" | Add-Content -Path "file.txt"

# Check if file exists
Test-Path -Path "C:\file.txt"
```

---

## Process Management

```powershell
# List all processes
Get-Process

# List specific process
Get-Process -Name "python"

# Kill process by name
Stop-Process -Name "notepad"

# Kill process by ID
Stop-Process -Id 1234

# Kill process forcefully
Stop-Process -Name "chrome" -Force

# Start process
Start-Process "notepad.exe"

# Start process with arguments
Start-Process "python.exe" -ArgumentList "script.py"

# Get CPU and memory usage
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Monitor process in real-time
while($true) {
    Get-Process | Sort-Object CPU -Descending | Select-Object -First 5
    Start-Sleep -Seconds 2
    Clear-Host
}
```

---

## Network Commands

```powershell
# Get IP configuration
Get-NetIPAddress

# Test network connection (ping)
Test-Connection google.com

# Test network connection (specific count)
Test-Connection google.com -Count 4

# Get network adapters
Get-NetAdapter

# Flush DNS cache
Clear-DnsClientCache

# Display DNS cache
Get-DnsClientCache

# Trace route
Test-NetConnection google.com -TraceRoute

# Test specific port
Test-NetConnection google.com -Port 443

# Get listening ports
Get-NetTCPConnection -State Listen

# Download file from web
Invoke-WebRequest -Uri "https://example.com/file.zip" -OutFile "file.zip"

# Check public IP
(Invoke-WebRequest -Uri "https://api.ipify.org").Content
```

---

## System Information

```powershell
# Get system info
Get-ComputerInfo

# Get OS version
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber

# Get hardware info
Get-CimInstance Win32_ComputerSystem

# Get disk space
Get-PSDrive -PSProvider FileSystem

# Get disk details
Get-Disk

# Get volume information
Get-Volume

# Get CPU info
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, MaxClockSpeed

# Get RAM info
Get-CimInstance Win32_PhysicalMemory | Select-Object Manufacturer, Capacity, Speed

# Get installed software
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion

# Get environment variables
Get-ChildItem Env:

# Get specific environment variable
$env:PATH

# Get uptime
(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
```

---

## User & Permission Management

```powershell
# Get current user
$env:USERNAME

# Get all local users
Get-LocalUser

# Get user groups
Get-LocalGroup

# Check if running as Administrator
([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

# Run as Administrator (restart PowerShell)
Start-Process powershell -Verb RunAs

# Get file permissions
Get-Acl -Path "C:\file.txt"
```

---

## Scheduled Tasks Management

```powershell
# List all scheduled tasks
Get-ScheduledTask

# Get specific task
Get-ScheduledTask -TaskName "DailyVocabularyMailer"

# Get task info
Get-ScheduledTaskInfo -TaskName "DailyVocabularyMailer"

# Run task immediately
Start-ScheduledTask -TaskName "DailyVocabularyMailer"

# Stop running task
Stop-ScheduledTask -TaskName "DailyVocabularyMailer"

# Enable task
Enable-ScheduledTask -TaskName "DailyVocabularyMailer"

# Disable task
Disable-ScheduledTask -TaskName "DailyVocabularyMailer"

# Delete task
Unregister-ScheduledTask -TaskName "DailyVocabularyMailer" -Confirm:$false

# Export task to XML
Export-ScheduledTask -TaskName "DailyVocabularyMailer" | Out-File "task.xml"

# Using schtasks command
schtasks /query                                    # List all tasks
schtasks /query /tn "TaskName" /fo LIST /v         # Detailed view
schtasks /run /tn "TaskName"                       # Run task
schtasks /end /tn "TaskName"                       # Stop task
schtasks /change /tn "TaskName" /disable           # Disable task
schtasks /change /tn "TaskName" /enable            # Enable task
schtasks /delete /tn "TaskName" /f                 # Delete task
```

---

## Service Management

```powershell
# List all services
Get-Service

# Get specific service
Get-Service -Name "Spooler"

# Start service
Start-Service -Name "Spooler"

# Stop service
Stop-Service -Name "Spooler"

# Restart service
Restart-Service -Name "Spooler"

# Set service startup type
Set-Service -Name "Spooler" -StartupType Automatic

# Check service status
(Get-Service -Name "Spooler").Status
```

---

## Python-Specific Commands

```powershell
# Check Python version
python --version

# Check Python location
(Get-Command python).Source

# List installed packages
python -m pip list

# Install package
python -m pip install package_name

# Uninstall package
python -m pip uninstall package_name

# Upgrade package
python -m pip install --upgrade package_name

# Install from requirements.txt
python -m pip install -r requirements.txt

# Freeze installed packages
python -m pip freeze > requirements.txt

# Show package info
python -m pip show package_name

# Check outdated packages
python -m pip list --outdated

# Create virtual environment
python -m venv venv_name

# Activate virtual environment
.\venv_name\Scripts\Activate.ps1

# Deactivate virtual environment
deactivate

# Run Python script
python script.py

# Run Python script with arguments
python script.py arg1 arg2

# Run Python module
python -m module_name
```

---

## PowerShell Script Execution

```powershell
# Check execution policy
Get-ExecutionPolicy

# Set execution policy (current user)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Set execution policy (all users - requires admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned

# Run PowerShell script
.\script.ps1

# Run script with parameters
.\script.ps1 -Param1 "value" -Param2 123

# Run script as administrator
Start-Process powershell -Verb RunAs -ArgumentList "-File `"$PWD\script.ps1`""
```

---

## Text Processing & Search

```powershell
# Search in file
Select-String -Path "file.txt" -Pattern "search_term"

# Search in multiple files
Get-ChildItem -Recurse -Filter *.txt | Select-String -Pattern "search_term"

# Count lines in file
(Get-Content "file.txt").Count

# Get first 10 lines
Get-Content "file.txt" -TotalCount 10

# Get last 10 lines
Get-Content "file.txt" -Tail 10

# Find and replace in file
(Get-Content "file.txt") -replace 'old', 'new' | Set-Content "file.txt"

# Compare files
Compare-Object (Get-Content "file1.txt") (Get-Content "file2.txt")
```

---

## System Maintenance

```powershell
# Clear temp files
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue

# Check disk
chkdsk C: /f

# System file checker
sfc /scannow

# DISM repair
DISM /Online /Cleanup-Image /RestoreHealth

# Shutdown computer
Stop-Computer

# Restart computer
Restart-Computer

# Shutdown with timer (seconds)
Stop-Computer -ComputerName localhost -Force

# Restart with timer
shutdown /r /t 300

# Cancel shutdown
shutdown /a

# Lock workstation
rundll32.exe user32.dll,LockWorkStation

# Clear screen
Clear-Host
# or
cls

# Get command history
Get-History

# Clear command history
Clear-History
```

---

## Useful Shortcuts & Aliases

```powershell
# Common aliases
ls        # Get-ChildItem
cd        # Set-Location
pwd       # Get-Location
cat       # Get-Content
rm        # Remove-Item
cp        # Copy-Item
mv        # Move-Item
mkdir     # New-Item -ItemType Directory
cls       # Clear-Host
type      # Get-Content
dir       # Get-ChildItem

# Create custom alias
Set-Alias -Name np -Value notepad

# View all aliases
Get-Alias

# Remove alias
Remove-Alias -Name np
```

---

## Date & Time

```powershell
# Get current date/time
Get-Date

# Format date
Get-Date -Format "yyyy-MM-dd"

# Get date components
(Get-Date).Year
(Get-Date).Month
(Get-Date).Day
(Get-Date).Hour

# Add days to date
(Get-Date).AddDays(7)

# Subtract days
(Get-Date).AddDays(-7)

# Calculate time difference
$start = Get-Date "2026-01-01"
$end = Get-Date
$diff = $end - $start
$diff.Days
```

---

## Windows Explorer Integration

```powershell
# Open current directory in Explorer
explorer .

# Open specific folder
explorer C:\Windows

# Open file location
explorer /select,"C:\path\to\file.txt"

# Open Control Panel directly to specific item
control /name Microsoft.System                    # System
control /name Microsoft.NetworkAndSharingCenter    # Network
control /name Microsoft.PowerOptions              # Power Options
```

---

## Quick System Operations

```powershell
# Open Notepad
notepad

# Open Calculator
calc

# Open Paint
mspaint

# Open Command Prompt
cmd

# Open Windows Terminal (if installed)
wt

# Open Registry Editor
regedit

# Run command
Start-Process "command"

# Open URL in default browser
Start-Process "https://google.com"

# Open file with default program
Invoke-Item "file.txt"
```

---

## Helpful Tips

### 1. Get help for any command
```powershell
Get-Help Get-Process
Get-Help Get-Process -Examples
Get-Help Get-Process -Full
```

### 2. Tab completion
Press `Tab` to autocomplete commands, file names, and paths

### 3. Pipeline
Chain commands together:
```powershell
Get-Process | Where-Object {$_.CPU -gt 100} | Sort-Object CPU -Descending
```

### 4. Export output
```powershell
Get-Process | Export-Csv -Path "processes.csv"
Get-Service | Export-Csv -Path "services.csv"
```

### 5. Measure execution time
```powershell
Measure-Command { python script.py }
```

---

**Last Updated:** January 21, 2026  
**PowerShell Version:** 5.1+ / 7.x

Yes, you can absolutely have multiple Windows Task Scheduler tasks with different time intervals. Each scheduled task operates independently with its own timing configuration.

For your vocabulary service, you could create multiple tasks such as:

VocabularyMailer_Morning - runs at 8:00 AM daily
VocabularyMailer_Evening - runs at 6:00 PM daily
VocabularyMailer_Weekly - runs every Sunday
VocabularyMailer_Hourly - runs every hour
Each task can:

Run the same script with different parameters
Run different scripts entirely
Have unique triggers (daily, weekly, hourly, on specific events)
Have different user accounts and permissions
Example commands to create multiple tasks:

# Morning task
schtasks /create /tn "VocabularyMailer_Morning" /tr "python C:\path\to\main.py" /sc daily /st 09:00

# Evening task  
schtasks /create /tn "VocabularyMailer_Evening" /tr "python C:\path\to\main.py" /sc daily /st 18:00

# Hourly task
schtasks /create /tn "VocabularyMailer_Hourly" /tr "python C:\path\to\main.py" /sc hourly