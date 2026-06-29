import asyncio
import websockets
import logging

logging.basicConfig(level=logging.INFO)

clients = {}

async def relay(websocket, path):
    client_id = id(websocket)
    clients[client_id] = websocket
    logging.info(f"Client connected: {client_id}")
    try:
        async for message in websocket:
            for cid, client in list(clients.items()):
                if cid != client_id:
                    try:
                        await client.send(message)
                    except:
                        del clients[cid]
    finally:
        del clients[client_id]
        logging.info(f"Client disconnected: {client_id}")

async def main():
    port = int(os.environ.get("PORT", 8080))
    async with websockets.serve(relay, "0.0.0.0", port):
        logging.info(f"Relay running on port {port}")
        await asyncio.Future()

asyncio.run(main())
