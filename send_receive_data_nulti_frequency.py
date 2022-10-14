import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX127x
import time
import csv
from os.path import exists
import pandas as pd

#####################################################################################################################################
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

#############################################################################################################
def compute_send_receive():
    while True:
        sent_counter = 0
        receive_counter = 0
        with open("/home/pi/data.csv",newline='') as csvfile:
            data = csv.reader(csvfile,delimiter=',')
            for row in data:
                if str(row[0]).startswith("Send"):
                    print("Switching to Send Mode, please wait 5 sec...")
                    ##############################################################################################
                    print("applying send setting")
                    time.sleep(5)
                    busId = 0; csId = 0
                    resetPin = 22; irqPin = -1; txenPin = -1; rxenPin = -1
                    LoRa = SX127x()
                    if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin):
                        raise Exception("Something wrong, can't begin LoRa radio")
                    print("Set frequency to 915 Mhz")
                    LoRa.setFrequency(150000000)
                    LoRa.setTxPower(17, LoRa.TX_POWER_PA_BOOST)
                    print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
                    LoRa.setSpreadingFactor(7)
                    LoRa.setBandwidth(125000)
                    LoRa.setCodeRate(5)
                    LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)
                    LoRa.setPreambleLength(12)
                    LoRa.setPayloadLength(100)
                    LoRa.setCrcEnable(True)
                    print("Set syncronize word to 0x34")
                    LoRa.setSyncWord(0x34)
                    ##############################################################################################
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
                    del LoRa
                elif str(row[0]).startswith("Receive"):
                    print("Switching to Receive Mode, please wait 5 sec...")
                    ##############################################################################################
                    print("applying send setting")
                    time.sleep(5)
                    busId2 = 0; csId2 = 0
                    resetPin2 = 22; irqPin2 = -1; txenPin2 = -1; rxenPin2 = -1
                    Two_LoRa = SX127x()
                    if not Two_LoRa.begin(busId2, csId2, resetPin2, irqPin2, txenPin2, rxenPin2):
                        raise Exception("Something wrong, can't begin LoRa radio")
                    print("Set frequency to 915 Mhz")
                    Two_LoRa.setFrequency(300000000)
                    Two_LoRa.setTxPower(17, Two_LoRa.TX_POWER_PA_BOOST)
                    print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
                    Two_LoRa.setSpreadingFactor(7)
                    Two_LoRa.setBandwidth(125000)
                    Two_LoRa.setCodeRate(5)
                    Two_LoRa.setHeaderType(Two_LoRa.HEADER_EXPLICIT)
                    Two_LoRa.setPreambleLength(12)
                    Two_LoRa.setPayloadLength(100)
                    Two_LoRa.setCrcEnable(True)
                    print("Set syncronize word to 0x34")
                    Two_LoRa.setSyncWord(0x34)
                    ##############################################################################################
                    time.sleep(5)
                    fields = ["column0",]
                    filename = "recevice_data.csv"
                    with open(filename,'a') as receivefile:
                        receive_writer = csv.writer(receivefile)
                        receive_writer.writerow(fields)
                        n=1
                        while n>0:
                            message11 = ""
                            while Two_LoRa.available() > 1 :
                                message11 += chr(Two_LoRa.read())
                                receive_writer.writerows(str(message11))
                            counter = Two_LoRa.read()
                            print("{} {}".format(message11,counter))
                            print("Packet status: RSSI = {0:0.2f} dBm | SNR = {1:0.2f} dB".format(Two_LoRa.packetRssi(), Two_LoRa.snr()))
                            status = Two_LoRa.status()
                            if status == Two_LoRa.STATUS_CRC_ERR : print("CRC error")
                            elif status == Two_LoRa.STATUS_HEADER_ERR : print("Packet header error")
                            n=0
                    del Two_LoRa
    #data.truncate()
    #data.close()

# Transmit message continuously
while True :
    if exists("/home/pi/data.csv") == True:
        print("File Present")
        compute_send_receive()
    else:
        no_data_sent("no_data")


