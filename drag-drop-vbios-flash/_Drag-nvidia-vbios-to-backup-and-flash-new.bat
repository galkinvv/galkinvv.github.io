@if x%1==x echo Drag a rom file over the shortcut to flash nvidia vbios && pause && exit
@if not exist "%~f1" echo "vbios file %~nx1 in the folder %~dp1 can't be used, place it in %~dp0 and try again" && pause && exit
@set run_as_admin_cmdline="%~f0" "%~f1" --no-elevate
@if x%2==x start "" "%~dp0\run_as_admin_cmdline.lnk" && exit || exit
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
call %flasher% --save %backup_name%
call %flasher% -6 "%~f1" -L con
@set FLASH_STATUS=%ERRORLEVEL%
@if %FLASH_STATUS%==0 (echo Finished. Window can be closed) else (echo Error code %FLASH_STATUS%. Window can be closed)

