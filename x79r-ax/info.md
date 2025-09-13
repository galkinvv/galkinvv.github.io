ISL6617CRZ Phase doubler

FDMF6705V DRMos

SRPG0603-r20 INDUCTOR (аналог IHLP-2525CZ)

16GB module 1600Mhz candidate: Crucial CT204864BD160B Micron C9BFJ (CT41K1 series CT41K1G8SN-107:A)

Stable flashing of W25Q64BV:
 * force PS_ON to GND - this gives 3.3V on the board without any SPI activity
 * connect 4 signal pins and GND to programmer, don't connect 3.3V. Switch programmer to 3.3V mode
 * use lower speeds to workaround bad fronts: `flashrom -c 'W25Q64BV/W25Q64CV/W25Q64FV'  -p ft2232_spi:type=2232H,port=B,divisor=10` for stable flashing
 
4MB HUANANZHI X79 deluxe HNX79V279/271K0035.bin with Xeon 2660 gives AMI picture and hangs aftewards.
