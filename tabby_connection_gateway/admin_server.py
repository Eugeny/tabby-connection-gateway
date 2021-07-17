import logging
from tabby_connection_gateway.gateway_server import GatewayServer
from .base import BaseServer, BaseWorker

log = logging.getLogger('server')


class AdminWorker(BaseWorker):
    async def start(self):
        await self.send_service_message(
            {
                '_': 'hello',
                'version': 1,
            }
        )
        msg = await self.recv_service_message()
        if msg.get('_') == 'authorize-client':
            token = msg.get('token')
            if not token:
                await self.fatal('expected-token')
            GatewayServer.authorized_tokens.add(token)
            self.log.info(f'Added a new auth token {token[:4]}***')
        else:
            await self.fatal('unexpected-command')


class AdminServer(BaseServer):
    async def handler(self, websocket):
        w = AdminWorker(websocket)
        await w.start()
        await w.wait()
        await w.close()
