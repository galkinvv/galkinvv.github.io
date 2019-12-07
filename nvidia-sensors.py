#!/usr/bin/env python3
# Dependencies: install python-smbus python package and i2cdetect binary (both from i2c-tools source)
# Copyright (C) 2019 Vasily Galkin (galkinvv.github.io)
# This file may be used and redistributed accorindg to
# SPDX-License-Identifier: GPL-3.0-only

import re
import sys
import subprocess

class INA3221:
	I2C_ADDR = 0x40
	MANUFACTURER_ID_VALUE = 0x5449 #Texas Instruments
	DIE_ID_VALUE = 0x3220 #INA 3221
	class Reg:
		MANUFACTURER_ID = 0xFE
		DIE_ID = 0xFF
		CH1_SHUNT = 0x1
		CH1_BUS = 0x2
		ShiftChannel = 0x2

	@staticmethod
	def read(bus, register):
		reved = bus.read_word_data(INA3221.I2C_ADDR, register)
		#reverse bytes in word
		return  int.from_bytes(reved.to_bytes(2, byteorder='little'), byteorder='big', signed=False)

def pretty_floats(float_arr):
	return ["{0:05.2f}".format(f) for f in float_arr]
def get_power_data(pci_id):
	import smbus
	subprocess.run(["modprobe", "i2c-dev"])
	i2c_devs = subprocess.run(["i2cdetect", "-l"], capture_output=True, text=True).stdout.splitlines()
	i2c_dev_selected = [i.split("\t")[0] for i in i2c_devs if "NVIDIA i2c adapter 2 at "+pci_id in i]
	if len(i2c_dev_selected) != 1:
		print("Failed finding i2c adapter for NVIDIA gpu at " + pci_id)
		return None
	i2c_dev = i2c_dev_selected[0]
	print("Using ", i2c_dev)
	i2c_num = int(i2c_dev.split('-')[-1])
	bus = smbus.SMBus(i2c_num)
	if (
		INA3221.read(bus, INA3221.Reg.DIE_ID) != INA3221.DIE_ID_VALUE
		or INA3221.read(bus, INA3221.Reg.MANUFACTURER_ID) != INA3221.MANUFACTURER_ID_VALUE
		):
		print("Unknown I2C device")
		return None
	shunts = {	
		"If all shunts r5":[1,1,1],
		"If shunts r5, r5, r2":[1,1,0]
	}
	powers = []
	for channel in range(3):
		shunt_millivolts_raw = INA3221.read(bus, INA3221.Reg.CH1_SHUNT + channel * INA3221.Reg.ShiftChannel)
		if shunt_millivolts_raw >= 0x8000: shunt_millivolts_raw -= 0x10000 #handle negative value during lite load
		shunt_millivolts = shunt_millivolts_raw * 5 / 1000.
		in_volts = INA3221.read(bus, INA3221.Reg.CH1_BUS + channel * INA3221.Reg.ShiftChannel)/1000.
		r2_r5_amps = [shunt_millivolts/2., shunt_millivolts/5.]
		r2_r5_powers = [in_volts * amps for amps in r2_r5_amps]
		powers.append(r2_r5_powers)
		print(
			*pretty_floats([in_volts]), " Volt (normal is 12.000)    [r2, r5]",
			*pretty_floats([shunt_millivolts]), "millivolts on shunt  ",
			pretty_floats(r2_r5_amps), "amps  ",
			pretty_floats(r2_r5_powers), "Watts")
	for sk, sv in shunts.items():
		watts = [powers[i][v] for i, v in enumerate(sv)]
		print(sk, pretty_floats(watts), " Total watts:", sum(watts))
	bus.close()

if len(sys.argv) != 2:
	print(
"""This program gets power info from nvidia GPUs using I2C busses provided by nvidia driver.
Direct I2C is risky and if something goes wrong

IT MAY BRICK YOUR DISPLAY OR GPU.

Use at your own risk!
Usage (as root): """+sys.argv[0]+""" PCI_ID
Where PCI_ID is id of nvidia gpu with ina3221 onboard chip, like 3:00
""")
	sys.exit(1)
try:
	get_power_data(sys.argv[1])
except:
	print("Error occured, are you runing as root and has python-smbus and i2cdetect installed?\n\n")
	raise
	
"""Example output for EVGA 980TI under load
Using  i2c-3
12.09  Volt (normal is 12.000)    [r2, r5] 15.76 millivolts on shunt   ['07.88', '03.15'] amps   ['95.25', '38.10'] Watts
12.17  Volt (normal is 12.000)    [r2, r5] 21.08 millivolts on shunt   ['10.54', '04.22'] amps   ['128.25', '51.30'] Watts
12.13  Volt (normal is 12.000)    [r2, r5] 38.44 millivolts on shunt   ['19.22', '07.69'] amps   ['233.10', '93.24'] Watts
If all shunts r5 [38.101376, 51.30028799999999, 93.240064]  Total watts: 182.641728
"""
