"""
Relays data from a serial data provider to a server and back.
"""

import serial
import sys


def printUsage():
    print("""
client.py
Writes data from a serial port to a file.

Usage:
    python client.py <serialPortPath> <baudRate> <filePath>

Explanation:
    * serialPortPath: A path to the serial port to the provider.
    * baudRate: Baud rate for the serial port.
    * filePath: The file to write to.

Examples:
    python client.py /dev/master 9600 data.bin
    """)


def readSerial(ser):
    byte = ser.read(1)
    print('[readSerial] ' + str(byte))
    return byte


def run(ser, file):
    while True:
        byte = readSerial(ser)
        file.write(byte)
        print('')


def main():
    if len(sys.argv) < 4:
        printUsage()
        sys.exit(1)

    [_, serialPortPath, baudRate, filePath] = sys.argv
    ser = serial.Serial(serialPortPath, baudRate)

    with open(filePath, 'ab') as file:
        run(ser, file)


if __name__ == '__main__':
    main()
