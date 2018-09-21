"""
Provides a stream of data to a serial port, for testing.
"""

import sys
import time
import serial

PAYLOAD_A = [b'C', b'A', b'F', b'E']
PAYLOAD_B = [b'Z', b'X', b'Y', b'W']
SLEEP_DURATION = 0.5


def printUsage():
    print("""
testprovider.py
Provides a stream of data to a serial port, for testing.

Usage:
  python testprovider.py <payloadName> <serialPortPath> <baudRate>

Explanation:
  * payloadName: Which test data set to send. ``a'' or ``b''.
  * serialPortPath: The path to the serial port to write to.
  * baudRate: The baud rate for the serial port.

Example:
  python testprovider.py a /dev/master 9600
    """)


def emit(payloadName, ser):
    while True:
        payload = None
        if payloadName == 'a':
            payload = PAYLOAD_A
        else:
            payload = PAYLOAD_B
        for item in payload:
            ser.write(item)
            print(f'{item}')
            time.sleep(SLEEP_DURATION)
        print('.')


def main():
    if len(sys.argv) < 4:
        printUsage()
        sys.exit(1)

    [_, payloadName, port, baudRate] = sys.argv

    print(f'Connecting to {port} at baud {baudRate}\n')
    ser = serial.Serial(port, baudRate)

    emit(payloadName, ser)


if __name__ == '__main__':
    main()
