# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries                        
"""
# Import Python System Libraries
import binascii
import py_compile
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
# Import messaging libraries
import json
import xxtea
import datetime

key = b"smartAgriculture"

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
BAND = 868.0
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, BAND)
rfm9x.tx_power = 23
prev_packet = None

display.fill(0)
display.text('RasPi LoRa', 35, 0, 1)
display.text(time.strftime("%H:%M:%S", time.localtime()), 35, 20, 1)
display.show()

contador = 0

while True:
    packet = None
    # draw a box to clear the image

    # check for packet rx
    packet = rfm9x.receive(with_header=True)
    # if packet is None:
    #     display.show()
    #     display.text('- Waiting for PKT -', 15, 20, 1)
    # else:
    if packet is not None:
        # Display the packet text and rssi
        # display.fill(0)
        print("packet: " + str(contador))
        contador += 1
        prev_packet = packet
        packet_text = str(prev_packet, "unicode_escape")

        doc = (json.loads(packet_text))
        print(json.dumps(doc, indent=4))

        tag = doc["tag"]
        battConnection = doc["bat"]["con"]
        battVoltage = doc["bat"]["vol"]
        locationLat = xxtea.decrypt(binascii.a2b_hex(doc["loc"]["lat"]),
                                    key,
                                    padding=False).decode("utf-8")
        locationLat = float(locationLat.rstrip("\x00"))
        locationLng = xxtea.decrypt(binascii.a2b_hex(doc["loc"]["lng"]),
                                    key,
                                    padding=False).decode("utf-8")
        locationLng = float(locationLng.rstrip("\x00"))
        satellites = xxtea.decrypt(binascii.a2b_hex(doc["loc"]["sat"]),
                                   key,
                                   padding=False).decode("utf-8")
        satellites = int(satellites.rstrip("\x00"))
        altitude = xxtea.decrypt(binascii.a2b_hex(doc["loc"]["alt"]),
                                 key,
                                 padding=False).decode("utf-8")
        altitude = float(altitude.rstrip("\x00"))
        age = doc["loc"]["age"]
        temperatureAir = doc["mea"]["tair"]
        humidityAir = doc["mea"]["hair"]
        humiditySoil = doc["mea"]["hsoi"]
        gpsDateTime = doc["time"]
        if gpsDateTime == "2000-00-00 00:00:00":
            gpsDateTime = "2000-01-01 00:00:00"
        dateTime = datetime.datetime.strptime(gpsDateTime, "%Y-%m-%d %H:%M:%S")
        print(dateTime.date())
        print(dateTime.time())

        print("tag: " + tag)
        print("satellites: " + str(satellites))
        print("lat: " + str(locationLat))
        print("lng: " + str(locationLng))
        print("alt: " + str(altitude))
        print("----------------")
        # display.text('RX: ', 0, 0, 1)
        # display.text(packet_text, 25, 0, 1)
        time.sleep(1)

    if not btnA.value:
        # Send Button A
        # display.fill(0)
        # button_a_data = bytes("Button A!\r\n", "utf-8")
        # rfm9x.send(button_a_data)
        # display.text('Sent Button A!', 25, 15, 1)
        if display._power:
            display.poweroff()
        else:
            display.poweron()
    elif not btnB.value:
        # Send Button B
        display.fill(0)
        button_b_data = bytes("Button B!\r\n", "utf-8")
        rfm9x.send(button_b_data)
        display.text('Sent Button B!', 25, 15, 1)
    elif not btnC.value:
        # Send Button C
        display.fill(0)
        button_c_data = bytes("Button C!\r\n", "utf-8")
        rfm9x.send(button_c_data)
        display.text('Sent Button C!', 25, 15, 1)

    # display.show()
    time.sleep(3)
