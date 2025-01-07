## How to apply modded EDID (most methods are model-agnostic)

#### Permanent variant: apply once to display hardware, use with any source
Note: plug display as a second to a PC via any cable, get it detected in monitors list. Before modding the picture would be black/broken, bad picture does NOT prevent writing modded EDID. Save original EDID backup before changing it.
Software to use:
* Windows + AMD/NVIDIA: Use EDWriter from https://www.monitortests.com/forum/Thread-EDID-DisplayID-Writer
  * Carefully select display to avoid flashing the wrong one, press "Read EDID"
  * Press "Save file...", save backup
  * Press "Load file...", agree if asked, press "Write EDID"
  * Intel GPUs are NOT supported for writing EDID. But they workd fine with already modded, so use another PC for modding or use Linux writer (below)
* Linux + AMD/NVIDIA/Intel: Use edid-checked-writer from https://github.com/galkinvv/edid-checked-writer (see manual there)

Possible outcomes:

* If the software succeeds all done!
* If the software reports that device is write-protected - you will need trivial extra device (the video signal is passing through) - the so called "HDMI lock emulator" in the role of writeable-EDID-injector between signal source and HDMI cable.
Cheapest one is in a picture below (no need to disassemble it, internals shown below just for reference).
Write EDID into it and always use the monitor with this emulator.

![](writable-edid-injector.jpg)

#### Software-level override on a single PC: use as a secondary monitor after OS booted (can't show BIOS)

* Windows: use Custom Resolution Utility from https://www.monitortests.com/forum/Thread-Custom-Resolution-Utility-CRU
  * plug display, start CRU utility, select correct display in the list
  * Use "Import..." button to load custom EDI file, press OK
  * Run "Restart64" utility to force PC rescan monitors
* Linux: 
  * place custom EDID file in `/usr/lib/firmware/edid/NAME.bin`
  * add parameter to kernel cmd line like `drm.edid_firmware=edid/NAME.bin`
  * distribution-specific: you may need adding the above file into list of files packed into initramfs, see https://wiki.archlinux.org/title/Kernel_mode_setting#Forcing_modes_and_EDID


## EDID files for Yamakasi Catleap Q270 27" 2560x1440
My no-audio, no-overclock instance was NOT write-protected, so just permanently written EDID into it. Not sure about general case, maybe some are write-protected.

Handles hdmi-single-link input from ~35 to ~55Hz. 60Hz is unstable/experimental/may depend on cable/source.

#### Modded for HDMI source + passive HDMI⇾DVI cable or single-link DVI
* RECOMMENDED [256 byte YamakasiQ270-54HZ2025.1-edid-256byte.bin](https://github.com/galkinvv/galkinvv.github.io/raw/refs/heads/master/displays/EDIDModToFixDualLink/YamakasiQ270-54HZ2025.1-edid-256byte.bin)
40Hz default + 50, 54Hz selectable on PC, for passive HDMI⇾DVI cable/converter

* FAILSAFE [256 byte YamakasiQ270-ANY40HZ2025.1-edid-256byte.bin](https://github.com/galkinvv/galkinvv.github.io/raw/refs/heads/master/displays/EDIDModToFixDualLink/YamakasiQ270-ANY40HZ2025.1-edid-256byte.bin)
40Hz only, failsafe, most universal, for any cable+video source capable outputting 2560x1440 at 161MHz pixel clock

  * FAILSAFE [128 byte YamakasiQ270-ANY40HZ2025.1-edid-128byte.bin](https://github.com/galkinvv/galkinvv.github.io/raw/refs/heads/master/displays/EDIDModToFixDualLink/YamakasiQ270-ANY40HZ2025.1-edid-128byte.bin)
40Hz only, like above, but cut to 128byte if software complaining to padding in the file

* EXPERIMENTAL [256 byte YamakasiQ270-60HZ2025.2-edid-256byte.bin](https://github.com/galkinvv/galkinvv.github.io/raw/refs/heads/master/displays/EDIDModToFixDualLink/YamakasiQ270-60HZ2025.2-edid-256byte.bin)
40Hz default + 50, 54, 56, 60Hz selectable on PC, for passive HDMI⇾DVI cable/converter. 60Hz is very unstable, try pressing power button on a monitor several times until it show normal picture instead of blackscreen. May be very problematic if video source autoselects 60Hz rate.

#### Dual-link-DVI only (discrete GPU with DVI port or active converter)
* ORIGINAL [256 byte YamakasiQ270-Original-edid-256byte.bin](https://github.com/galkinvv/galkinvv.github.io/raw/refs/heads/master/displays/EDIDModToFixDualLink/YamakasiQ270-Original-edid-256byte.bin)
 60Hz, for physically Dual-link DVI only


For the latest version of this manual see https://github.com/galkinvv/galkinvv.github.io/tree/master/displays/EDIDModToFixDualLink#readme