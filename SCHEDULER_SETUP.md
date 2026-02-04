# Daily Vocabulary Service - Scheduler Setup Guide

## Overview
This document explains the PowerShell commands used to set up an automated scheduled task for the Daily Vocabulary Service. The task runs `task_handler.py` twice daily to send vocabulary emails to subscribers.

---

## Initial Setup - Dependency Installation

### Problem Encountered
When first running `task_handler.py` on Python 3.13, the following errors occurred:
1. Missing `pip` module in Python 3.13
2. Missing `tzdata` package (required for timezone support on Windows)
3. Missing other dependencies from `requirements.txt`

### Solution Commands

#### 1. Install pip for Python 3.13
```powershell
python -m ensurepip --upgrade
```

#### 2. Install tzdata (timezone support)
```powershell
python -m pip install tzdata
```

#### 3. Install all project dependencies
```powershell
python -m pip install streamlit fastapi uvicorn requests httpx gtts pythonturtle pyttsx3 openpyxl python-dotenv
```

**Note:** The `playsound` package was excluded due to compatibility issues with Python 3.13.

---

## Scheduled Task Configuration

### Current Setup
- **Task Name:** `DailyVocabularyMailer`
- **Frequency:** Twice daily (every 12 hours)
- **Times:** 8:00 AM and 8:00 PM
- **Python Executable:** `C:\Users\user2\AppData\Local\Programs\Python\Python313\python.exe`
- **Script Path:** `C:\Users\user2\Desktop\daily_vocabulary_service-main\task_handler.py`

### PowerShell Command to Create the Scheduled Task

```powershell
$action = New-ScheduledTaskAction `
    -Execute "C:\Users\user2\AppData\Local\Programs\Python\Python313\python.exe" `
    -Argument "task_handler.py" `
    -WorkingDirectory "C:\Users\user2\Desktop\daily_vocabulary_service-main"

$trigger1 = New-ScheduledTaskTrigger -Daily -At 8:00AM
$trigger2 = New-ScheduledTaskTrigger -Daily -At 8:00PM

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName "DailyVocabularyMailer" `
    -Action $action `
    -Trigger @($trigger1, $trigger2) `
    -Settings $settings `
    -Description "Sends vocabulary emails to subscribers twice daily (8 AM and 8 PM)"
```

---

## Task Management Commands

### View Task Details
```powershell
schtasks /query /tn "DailyVocabularyMailer" /fo LIST /v
```

### Run Task Immediately (Manual Test)
```powershell
schtasks /run /tn "DailyVocabularyMailer"
```

### Delete the Scheduled Task
```powershell
schtasks /delete /tn "DailyVocabularyMailer" /f
```

### Modify Task Schedule Time
Change to run at 10:00 AM instead of 8:00 AM:
```powershell
schtasks /change /tn "DailyVocabularyMailer" /st 10:00
```

### Disable the Task
```powershell
schtasks /change /tn "DailyVocabularyMailer" /disable
```

### Enable the Task
```powershell
schtasks /change /tn "DailyVocabularyMailer" /enable
```

---

## Alternative: Single Daily Execution

If you want to change back to running once per day at 9:00 AM:

```powershell
# Delete existing task
schtasks /delete /tn "DailyVocabularyMailer" /f

# Create new task with single daily trigger
schtasks /create /tn "DailyVocabularyMailer" `
    /tr "C:\Users\user2\AppData\Local\Programs\Python\Python313\python.exe C:\Users\user2\Desktop\daily_vocabulary_service-main\task_handler.py" `
    /sc daily /st 09:00 /f
```

---

## Troubleshooting

### Check if Python is in PATH
```powershell
(Get-Command python).Source
```

### Check Python Version
```powershell
python --version
```

### Check Installed Packages
```powershell
python -m pip list
```

### View Task Scheduler GUI
```powershell
taskschd.msc
```
Navigate to: Task Scheduler Library → Find "DailyVocabularyMailer"

### Check Task History
1. Open Task Scheduler GUI (`taskschd.msc`)
2. Find the task "DailyVocabularyMailer"
3. Click on the "History" tab at the bottom
4. Look for event IDs:
   - **100**: Task Started
   - **102**: Task Completed
   - **103**: Action Started
   - **201**: Action Completed Successfully

---

## Task Settings Explained

| Setting | Value | Purpose |
|---------|-------|---------|
| `-AllowStartIfOnBatteries` | Enabled | Allows task to run even when on battery power |
| `-DontStopIfGoingOnBatteries` | Enabled | Keeps task running if computer switches to battery |
| `-StartWhenAvailable` | Enabled | Runs task as soon as possible if a scheduled start is missed |
| `-WorkingDirectory` | Project folder | Ensures script can find relative files (JSON, etc.) |

---

## Notes

- The task runs under the current user account (`user2`)
- No password is required since the task uses the current user's context
- The task will run whether the user is logged in or not (if properly configured)
- Working directory is critical - the script needs to access JSON files in the project folder
- Multiple triggers (8 AM and 8 PM) are configured as separate trigger objects

---

## Verification Steps

After setting up the task:

1. **Verify task creation:**
   ```powershell
   schtasks /query /tn "DailyVocabularyMailer"
   ```

2. **Test run manually:**
   ```powershell
   schtasks /run /tn "DailyVocabularyMailer"
   ```

3. **Check task result:**
   ```powershell
   schtasks /query /tn "DailyVocabularyMailer" /fo LIST /v | Select-String "마지막 결과"
   ```
   A result of `0` indicates success.

4. **View in GUI:**
   ```powershell
   taskschd.msc
   ```

---

## Files Modified by task_handler.py

When the scheduled task runs, it modifies these JSON files:
- `mailed.json` - Tracks which words have been sent
- `subscribers_by_level.json` - Organizes subscribers by level
- Potentially `selected_level1.json`, `selected_level2.json`, `selected_level3.json`

Make sure these files are not locked or in use when the task runs.

---

**Last Updated:** January 21, 2026  
**Python Version:** 3.13.3  
**Task Status:** Active - Running twice daily at 8:00 AM and 8:00 PM
