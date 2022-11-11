@set run_as_admin_cmdline="%~f0" --no-elevate
@if x%1==x start "" "%~dp0\run_as_admin_cmdline.lnk" && exit || exit
@set now=%date:.=-%_%time::=%
@set now=%now: =%
@set now=%now:,=%
@set now=%now:/=%
@set now=%now:\=%
@set backup_name=vbios_backups/vbios_backup-%now:~0,17%.rom
@cd /d "%~dp0"
@if not exist vbios_backups mkdir vbios_backups
@set flasher=nvflash.exe
@if not exist %flasher% set flasher=nvflash64.exe
@call %flasher% --save %backup_name%
@call %flasher% --list
@set FLASH_STATUS=%ERRORLEVEL%
@call %flasher% --protectinfo
@if %FLASH_STATUS%==0 (echo Finished. Window can be closed) else (echo Error code %FLASH_STATUS% during list. Window can be closed)
@pause
