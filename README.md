# LORA_COMM
Low Powered Lora Communication Setup


Installation
Using pip
Using terminal run following command.

pip3 install LoRaRF
Using Git and Build Package
To using latest update of the library, you can clone then build python package manually. Using this method require setuptools and wheel module.

git clone https://github.com/chandrawi/LoRaRF-Python.git
cd LoRaRF-Python
python3 setup.py bdist_wheel
pip3 install dist/LoRaRF-1.3.0-py3-none-any.whl
Initialization
To work with the library, first you must import SX126x or SX127x python module depending LoRa module you use. Then initialize the module by creating an object.

# for SX126x series or LLCC68
from LoRaRF import SX126x
LoRa = SX126x()

# for SX127x series
from LoRaRF import SX127x
LoRa = SX127x()
Before calling any configuration methods, doing transmit or receive operation you must call begin() method.

LoRa.begin()
Hardware Configuration
Wiring Connections
Power pins, SPI pins, RESET, and BUSY pins must be connected between host controller and LoRa module. If you want to use interrupt operation, you can connect one of DIO1, DIO2, or DIO3 pin. You also should connect TXEN and RXEN pins if your LoRa module have those pins.

The default SPI port is using bus id 0 and cs id 0. The default GPIO pins used for connecting to SX126x and SX127x with Broadcom pin numbering are as follows.

Semtech SX126x	Semtech SX127x	Raspberry Pi
VCC	VCC	3.3V
GND	GND	GND
SCK	SCK	GPIO 11
MISO	MISO	GPIO 9
MOSI	MOSI	GPIO 10
NSS	NSS	GPIO 8
RESET	RESET	GPIO 22
BUSY		GPIO 23
DIO1	DIO1	-1 (unused)
TXEN	TXEN	-1 (unused)
RXEN	RXEN	-1 (unused)
SPI Port Configuration
To configure SPI port or SPI frequency call setSPI() method before begin() method.

# set to use SPI with bus id 0 and cs id 1 and speed 7.8 Mhz
LoRa.setSPI(0, 0, 7800000)
LoRa.begin()
I/O Pins Configuration
To configure I/O pins (NSS, RESET, BUSY, IRQ, TXEN, RXEN pin) call setPins() before begin() method.

# set RESET->22, BUSY->23, DIO1->26, TXEN->5, RXEN->25
LoRa.setPins(22, 23, 26, 5, 25)
LoRa.begin()
Modem Configuration
Before transmit or receive operation you can configure transmit power and receive gain or matching frequency, modulation parameter, packet parameter, and synchronize word with other LoRa device you want communicate.

Transmit Power
# set transmit power to +22 dBm for SX1262
LoRa.setTxPower(22, LoRa.TX_POWER_SX1262)
Receive Gain
# set receive gain to power saving
LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING)
Frequency
# Set frequency to 915 Mhz
LoRa.setFrequency(915000000)
Modulation Parameter
# set spreading factor 8, bandwidth 125 kHz, coding rate 4/5, and low data rate optimization off
LoRa.setLoRaModulation(8, 125000, 5, False)
Packet Parameter
# set explicit header mode, preamble length 12, payload length 15, CRC on and no invert IQ operation
LoRa.setLoRaPacket(LoRa.HEADER_EXPLICIT, 12, 15, true, False)
Synchronize Word
# Set syncronize word for public network (0x3444)
LoRa.setSyncWord(0x3444)
Transmit Operation
Transmit operation begin with calling beginPacket() method following by write() method to write package to be tansmitted and ended with calling endPacket() method. For example, to transmit "HeLoRa World!" message and an increment counter you can use following code.

# message and counter to transmit
message = "HeLoRa World!\0"
messageList = list(message)
for i in range(len(messageList)) : messageList[i] = ord(messageList[i])
counter = 0

LoRa.beginPacket()
LoRa.write(message, sizeof(message)) # write multiple bytes
LoRa.write(counter)                  # write single byte
LoRa.endPacket()
LoRa.wait()
counter += 1
For more detail about transmit operation, please visit this link.

Receive Operation
Receive operation begin with calling request() method following by read() method to read received package. available() method can be used to get length of remaining package. For example, to receive message and a counter in last byte you can use following code.

LoRa.request()
LoRa.wait()

# get message and counter in last byte
message = ""
while LoRa.available() > 1 :
  message += chr(LoRa.read())        # read multiple bytes
counter = LoRa.read()                # read single byte