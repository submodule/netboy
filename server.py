from asyncio import Queue
from collections import defaultdict
import asyncio
import websockets
import uuid

WS_HOST = 'localhost'
WS_PORT = 1337
clients = dict()
queues = defaultdict(Queue)


def isStop(val):
    return val == 'STOP'


async def run(websocket, cid):
    key = await websocket.recv()
    print(f'[run] {cid}@{key} Received server key')
    queue = queues[key]

    async def send():
        val = await queue.get()
        queue.task_done()
        print(f'[run] {cid}@{key} queue -> {val}')
        await websocket.send(val)

    async def recv():
        val = await websocket.recv()
        print(f'[run] {cid}@{key} queue <- {val}')
        await queue.put(val)
        print(f'[run] {cid}@{key} Joining')
        await queue.join()

    if queue.empty():
        print(f'[run] {cid}@{key} Queue empty, receiving')
        await recv()

    while True:
        await send()
        await recv()


async def handler(websocket, path):
    clientId = str(uuid.uuid4())[0:6]
    print(f'[handler] Client connected: {clientId}')
    clients[clientId] = websocket

    try:
        await run(websocket, clientId)
    except Exception as e:
        print('[handler] (exception) ' + str(e))
    finally:
        clients.pop(clientId, None)


def main():
    start_server = websockets.serve(handler, WS_HOST, WS_PORT)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
