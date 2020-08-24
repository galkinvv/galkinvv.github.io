@if x%1==x echo Drag a rom file over the shortcut to flash amd vbios && pause && exit
@if not exist "%~f1" echo "vbios file %~nx1 in the folder %~dp1 can't be used, place it in %~dp0 and try again" && pause && exit
@set run_as_admin_cmdline="%~f0" "%~f1" --no-elevate
@if x%2==x start "" "%~dp0\run_as_admin_cmdline.lnk" && exit
@set now=%date:.=-%_%time::=%
@set now=%now: =%
@set now=%now:,=%
@set now=%now:/=%
@set now=%now:\=%
@set backup_name=vbios_backup-%now:~0,17%.rom
@cd "%~dp0"
@set flasher=atiflash.exe
@if not exist %flasher% set flasher=amdvbflash.exe
call %flasher% -s 0 %backup_name%
call %flasher% -fs -fp -fa -p 0 %~f1
@echo Finished. Window can be closed
