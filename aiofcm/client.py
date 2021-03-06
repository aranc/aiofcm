import asyncio
from typing import Optional, NoReturn

from aiofcm.connection import FCMConnectionPool
from aiofcm.common import Message, MessageResponse
from aiofcm.logging import logger


class FCM:
    def __init__(self, sender_id, api_key, upstream_callback=None,
                 min_connections=None, max_connections=10, loop=None):
        if min_connections is None:
            min_connections = 1 if upstream_callback else 0

        # type: (int, str, callback, int int,
        #        Optional[asyncio.AbstractEventLoop]) -> NoReturn
        self.pool = FCMConnectionPool(sender_id, api_key, upstream_callback,
                                      min_connections, max_connections, loop)

    async def send_message(self, message: Message) -> MessageResponse:
        response = await self.pool.send_message(message)
        if not response.is_successful:
            msg = 'Status of message %s is %s' %\
                  (message.message_id, response.status)
            if response.description:
                msg += ' (%s)' % response.description
            logger.error(msg)
        return response
