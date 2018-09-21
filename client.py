"""
Relays data from a serial data provider to a server and back.
"""

import serial
import sys
import asyncio
import websockets


def printUsage():
    print("""
client.py
Relays data from a serial data provider to a server and back.

Usage:
    python client.py <kind> <serialPortPath> <baudRate>
        <serverHost> <serverPort> <serverKey>

Explanation:
    * kind:
        1. ``master'' or ``slave''. In a pair of clients, one should be
            master, one slave.
        2. Alternatively, ``oneway''. This means the client only sends
            data to the server.
    * serialPortPath: A path to the serial port to the provider.
    * baudRate: Baud rate for the serial port.
    * serverHost: The host of the websocket server.
    * serverPort: The port of the websocket server.
    * serverKey: A key that identifies the server session.

Examples:
    python client.py master /dev/master 9600 localhost 1337 cafe
    """)


async def readServer(websocket):
    val = await websocket.recv()
    print(f'[readServer] {val}')
    return val


async def writeServer(websocket, data):
    print('[writeServer] ' + str(data))
    await websocket.send(str(data))


def readProvider(ser):
    byte = ser.read(1)
    print('[readProvider] ' + str(byte))
    return byte


def writeProvider(ser, data):
    print('[writeProvider] ' + str(data))
    # ser.write(data)


async def run(kind, ser, websocket, serverKey):
    print(f'[run] Sending server key: {serverKey}')
    await websocket.send(kind)
    await websocket.send(serverKey)
    while True:
        if kind == 'master':
            ourByte = readProvider(ser)
            await writeServer(websocket, ourByte)
            theirByte = await readServer(websocket)
            writeProvider(ser, theirByte)
        elif kind == 'slave':
            theirByte = await readServer(websocket)
            writeProvider(ser, theirByte)
            ourByte = readProvider(ser)
            await writeServer(websocket, ourByte)
        elif kind == 'oneway':
            ourByte = readProvider(ser)
            await writeServer(websocket, ourByte)
        print('')


def main():
    if len(sys.argv) < 7:
        printUsage()
        sys.exit(1)

    [
        _, kind, serialPortPath, baudRate, serverHost, serverPort, serverKey
    ] = sys.argv
    wsUrl = f'ws://{serverHost}:{serverPort}'
    ser = serial.Serial(serialPortPath, baudRate)

    async def connectAndRun():
        async with websockets.connect(wsUrl) as websocket:
            print('[connectAndRun] Connected')
            await run(kind, ser, websocket, serverKey)

    asyncio.get_event_loop().run_until_complete(connectAndRun())


if __name__ == '__main__':
    main()
