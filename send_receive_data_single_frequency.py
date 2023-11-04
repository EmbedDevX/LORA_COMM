import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX127x
import time
import csv
from os.path import exists
import pandas as pd


# Begin LoRa radio and set NSS, reset, busy, IRQ, txen, and rxen pin with connected Raspberry Pi gpio pins
# IRQ pin not used in this example (set to -1). Set txen and rxen pin to -1 if RF module doesn't have one
busId = 0; csId = 0
resetPin = 22; irqPin = -1; txenPin = -1; rxenPin = -1
LoRa = SX127x()
print("Begin LoRa radio")
if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin) :
    raise Exception("Something wrong, can't begin LoRa radio")

# Set frequency to 915 Mhz
print("Set frequency to 915 Mhz")
LoRa.setFrequency(150000000)

# Set TX power, this function will set PA config with optimal setting for requested TX power
print("Set TX power to +17 dBm")
LoRa.setTxPower(17, LoRa.TX_POWER_PA_BOOST)                     # TX power +17 dBm using PA boost pin

# Configure modulation parameter including spreading factor (SF), bandwidth (BW), and coding rate (CR)
# Receiver must have same SF and BW setting with transmitter to be able to receive LoRa packet
print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
LoRa.setSpreadingFactor(7)                                      # LoRa spreading factor: 7
LoRa.setBandwidth(125000)                                       # Bandwidth: 125 kHz
LoRa.setCodeRate(5)                                             # Coding rate: 4/5

# Configure packet parameter including header type, preamble length, payload length, and CRC type
# The explicit packet includes header contain CR, number of byte, and CRC type
# Receiver can receive packet with different CR and packet parameters in explicit header mode
#print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)                        # Explicit header mode
LoRa.setPreambleLength(12)                                      # Set preamble length to 12
LoRa.setPayloadLength(100)                                       # Initialize payloadLength to 15
LoRa.setCrcEnable(True)                                         # Set CRC enable

# Set syncronize word for public network (0x34)
print("Set syncronize word to 0x34")
LoRa.setSyncWord(0x34)

#print("\n-- LoRa Transmitter --\n")
#counter = 0

def compute_send_receive():
    while True:
        sent_counter = 0
        receive_counter = 0
        with open("/home/pi/data.csv",newline='') as csvfile:
            data = csv.reader(csvfile,delimiter=',')
            for row in data:
                if str(row[0]).startswith("Send"):
                    print("Switching to Send Mode, please wait 5 sec...")
                    time.sleep(5)
                    message = str(row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+",")
                    messageList = list(message)
                    for i in range(len(messageList)) : messageList[i] = ord(messageList[i])
                    LoRa.beginPacket()
                    LoRa.write(messageList, len(messageList))
                    LoRa.write([sent_counter], 1)
                    LoRa.endPacket()
                    print("{} {}".format(message,sent_counter))
                    LoRa.wait()
                    print("Transmit time: {0:0.2f} ms | Data rate: {1:0.2f} byte/s".format(LoRa.transmitTime(), LoRa.dataRate()))
                    time.sleep(5)
                    sent_counter = (sent_counter + 1) % 256
                elif str(row[0]).startswith("Receive"):
                    fields = ["column0",]
                    filename = "recevice_data.csv"
                    with open(filename,'a') as receivefile:
                        receive_writer = csv.writer(receivefile)
                        receive_writer.writerow(fields)
                        print("Switching to Receive Mode, please wait 5 sec...")
                        time.sleep(5)
                        n=1
                        while n>0:
                            message = ""
                            while LoRa.available() > 1 :
                                message += chr(LoRa.read())
                                receive_writer.writerows(str(message))
                            counter = LoRa.read()
                            print("{} {}".format(message,counter))
                            print("Packet status: RSSI = {0:0.2f} dBm | SNR = {1:0.2f} dB".format(LoRa.packetRssi(), LoRa.snr()))
                            status = LoRa.status()
                            if status == LoRa.STATUS_CRC_ERR : print("CRC error")
                            elif status == LoRa.STATUS_HEADER_ERR : print("Packet header error")
                            n=0

    #data.truncate()
    #data.close()
def no_data_sent(message_data= "no_data"):
    while True:
        message = message_data
        msglist = list(message)
        for i in range(len(msglist)) : msglist[i] = ord(msglist[i])
        LoRa.beginPacket()
        LoRa.write(msglist,len(messageList))
        LoRa.write([counter],1)
        LoRa.endPacket()
        print("{} {}".format(message,counter))
        LoRa.wait()
        print("Transmit time: {0:0.2f} ms | Data rate: {1:0.2f} byte/s".format(LoRa.transmitTime(), LoRa.dataRate()))
        time.sleep(5)
        counter = (counter +1) %256


# Transmit message continuously
while True :
    if exists("/home/pi/data.csv") == True:
        print("File Present")
        compute_send_receive()
    else:
        no_data_sent("no_data")
        print("")

