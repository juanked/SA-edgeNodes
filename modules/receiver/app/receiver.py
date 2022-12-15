# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import os
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
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
from EdgeNodeConfiguration import *
from ActuatorConfiguration import *
from MQTTConnection import *
from Telemetry import *
from dataSuplier import *
from edgeProcessor import *

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

alo = "google.com"  # example
response = os.system("ping -c 1 " + alo)

# and then check the response...
if response == 0:
    print(f"{alo}, is up!")
else:
    print(f"{alo}, is down!")
# getClientInformation
c = 0
hostname = os.environ['NODE_NAME']
edgeNodeID = getEdgeNodeID(hostname)

while edgeNodeID == -1:
    edgeNodeID = getEdgeNodeID(hostname)
    time.sleep(10)
    c += 1
    if c > 20:
        break

contador = 0

while True:
    if not btnA.value:
        if display._power:
            display.poweroff()
        else:
            display.poweron()
    time.sleep(1)

    packet = None
    packet = rfm9x.receive(with_header=True)

    if packet is None:
        time.sleep(3)
        continue
    if prev_packet == packet:
        time.sleep(3)
        continue
    prev_packet = packet
    packet_text = str(prev_packet, "unicode_escape")

    if "#" not in packet_text:
        time.sleep(3)
        continue

    print("packet: " + str(contador))
    contador += 1
    cryptMessage = packet_text.split("#")
    serial = cryptMessage[0]
    edgeConfig = searchConfig(serial, edgeNodeID)
    if edgeConfig is None:
        print("edgeConfig=None")
        time.sleep(3)
        continue
    try:
        decryptMessage = xxtea.decrypt(binascii.a2b_hex(
            cryptMessage[1]), key, padding=False).decode("utf-8")
    except binascii.Error as e:
        print(e)
        time.sleep(3)
        continue
    print(decryptMessage)
    decryptMessage = decryptMessage.split(";")
    soilMoisture = int(decryptMessage[8])
    leafMoisture = bool(int(decryptMessage[9]))
    print("Leaf moisture: ", end="")
    print(leafMoisture)
    telemetry = Telemetry(bool(decryptMessage[0]), float(decryptMessage[1]), float(decryptMessage[2]),
                          float(decryptMessage[3]), float(decryptMessage[4]),
                          int(decryptMessage[5]), float(decryptMessage[6]),
                          float(decryptMessage[7]), float(moistureConverter(
                              soilMoisture, edgeConfig.sensorLinearFit)),
                          float(edgeConfig.fieldCapacity), leafMoisture)
    plantationID = edgeConfig.plantationID
    actuators = searchActuators(plantationID)

    mqtt = searchMQTT(plantationID)
    if mqtt is None:
        print("mqtt=None")
        time.sleep(3)
        continue
    client = TBDeviceMqttClient(host=mqtt.host, port=mqtt.port,
                                client_id=mqtt.clientID, username=mqtt.username, password=mqtt.pwd, quality_of_service=1)
    try:
        client.connect()
        print(telemetry.getTelemetry())
        result = client.send_telemetry(telemetry.getTelemetry())
        success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
        print("success: ", end="")
        print(success)
        if actuators is None:
            client.disconnect()
            time.sleep(3)
            continue
        wateringNecessary = isWateringNecessary(
            edgeConfig, telemetry.airTemperature, telemetry.airHumidity, soilMoisture, telemetry.leafMoisture)
        packetToSend = watering(actuators, wateringNecessary, key)
        print("Wattering necessary: ", end="")
        print(wateringNecessary)
        for element in packetToSend:
            print("Paquete a enviar: ", end="")
            print(element)
            rfm9x.send(bytes(element, "utf-8"))
        # client.connect()
        result = client.send_telemetry({"isWatering": wateringNecessary})
        success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
        client.disconnect()
    except OSError as e:
        print("Error during MQTT connection")
        print(e)

    time.sleep(3)

    # elif not btnB.value:
    #     # Send Button B
    #     display.fill(0)
    #     button_b_data = bytes("Button B!\r\n", "utf-8")
    #     rfm9x.send(button_b_data)
    #     display.text('Sent Button B!', 25, 15, 1)
    # elif not btnC.value:
    #     # Send Button C
    #     display.fill(0)
    #     button_c_data = bytes("Button C!\r\n", "utf-8")
    #     rfm9x.send(button_c_data)
    #     display.text('Sent Button C!', 25, 15, 1)

    # display.show()
