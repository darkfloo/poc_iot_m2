# -*- coding: utf-8 -*-
import logging
import asyncio
from pickle import FALSE
import platform
import struct
import requests
from bleak import BleakClient

########################################
# BLE datas

# UUID de la led
_LED_UUID = "20000000-0001-11E1-AC36-0002A5D5C51B"
# UUID des capteurs
SENSOR_UUID = "001c0000-0001-11e1-ac36-0002a5d5c51b"

ADDRESS = (
    "02:09:13:5D:36:F2"                         # <--- Change to your device's address here if you are using Windows or Linux
    if platform.system() != "Darwin"
    else "912F882D-4526-2084-25E2-93212D83D758" # <--- Change to your device's address here if you are using macOS
)

########################################
# MQTT datas

accesstoken='Y08ALatJF3U8j41lt6Dr'
host = f"https://im2ag-thingboard.univ-grenoble-alpes.fr/api/v1/{accesstoken}/telemetry"

# Coroutine handling BLE
async def run(address, debug=False):
	print("Bleak connects..")

	async with BleakClient(address) as bleak_client:
		print(f"Bleak connected: {bleak_client}")

		def notification_handler(sender, data):
			timestamp, pressure, humidity, temperature,analog= struct.unpack('<HiHhH', data)
			msg = {'timestamp': timestamp,  'pressure':pressure/100, 'humidity':humidity , 'temperature':temperature,'analog':analog}
			print(host)
			print(msg)
			r = requests.post(host, json=msg, verify='./chain.pem')

		await bleak_client.start_notify(SENSOR_UUID, notification_handler)
		print("Start notify ok")
		try:
			while True:
				await asyncio.sleep(1)
		except asyncio.CancelledError:
			print("Shutdown Request Received")
		print("Stop")
		await bleak_client.stop_notify(SENSOR_UUID)
			
			
# Starts BLE handling
loop = asyncio.get_event_loop()
loop.run_until_complete(run(ADDRESS))
		
