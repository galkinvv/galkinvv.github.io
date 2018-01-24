@if x%1==x echo Drag a rom file over the shortcut to flash amd vbios && pause && exit
@if not exist "%~f1" echo "vbios file %~nx1 in the folder %~dp1 can't be used, place it in %~dp0 and try again" && pause && exit
@set amd_vbios_cmdline="%~f0" "%~f1" --no-elevate
@if x%2==x start "" "%~dp0\run-amd-vbios-as-admin.lnk" && exit
@call "%~dp0\atiflash.exe" -ai 0
@echo Finished. Window can be closed