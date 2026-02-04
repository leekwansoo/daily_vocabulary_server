@echo off
echo Creating scheduled task for VocabularyViewTrigger...

powershell -Command "$action = New-ScheduledTaskAction -Execute 'C:\Users\user2\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe' -Argument 'run trigger.py' -WorkingDirectory 'C:\Users\user2\Desktop\daily_vocabulary_service-main'; $trigger = New-ScheduledTaskTrigger -Daily -At 14:30; $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable; Register-ScheduledTask -TaskName 'VocabularyViewTrigger' -Action $action -Trigger $trigger -Settings $settings -Description 'Triggers vocabulary viewer daily at 14:30 using Streamlit'"

echo.
echo Task created successfully!
echo To verify, run: schtasks /query /tn "VocabularyViewTrigger" /fo LIST
pause