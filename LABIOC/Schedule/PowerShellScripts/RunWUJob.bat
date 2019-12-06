for /F "usebackq" %%i IN (`powershell -ExecutionPolicy Bypass get-date -format "dd"`) do set day=%%i
set LogFolder=%~dp0
if not exist %LogFolder% (mkdir %LogFolder%)
powershell -ExecutionPolicy Bypass %~dp0WUJob.ps1 >%LogFolder%\WUJob_%day%.log