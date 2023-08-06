import logging
import time

import requests
import trio
from trio_websocket import connect_websocket_url, ConnectionClosed


from . import responses
from .commands import new, ping, hello, resume
from .events import Event
from .message import pack, unpack
from .urls import me, ribbon

logger = logging.getLogger(__name__)


async def msgHandle(ws, msg):
    bot = ws.bot
    if isinstance(msg, tuple):  # if the message has an id
        msgId = msg[0]
        bot.serverId += 1
        msg = msg[1]
        msg['id'] = msgId
        logServer(msg, ws)
    if isinstance(msg, list):  # multiple messages that should be handled
        for m in msg:
            await msgHandle(ws, m)
        return
#    print(f'parsing command {msg["command"]}')
    comm = msg['command'].split('.')[0]
#    print(comm)
    logger.info(f'got {comm} command')
    try:
        func = responses.__dict__[comm]
    except:
        logger.info(f'unrecognized command {comm}')
        return
#    print(comm, func)
    await func(bot, msg, msgHandle)


class Message:
    def __init__(self, message):
        self.time = time.time()
        self.id = message['id']
        self.message = message

    def checkTime(self, t):
        return time.time() - self.time >= t


def log(msg, ws):
    bot = ws.bot
    messages = bot.messages
    messages.append(Message(msg))  # log the new message
    logFor = 30  # seconds
    for message in messages:
        remove = message.checkTime(logFor)
        if remove:
            messages.pop(0)  # remove the first message if needed
        else:
            break
    bot.messages = messages


def logServer(msg, ws):
    #    print(f'logging message {msg}')
    bot = ws.bot
    messages = bot.serverMessages
    messages.append(Message(msg))  # log the new message
    logFor = 30  # seconds
    for message in messages:
        if message.checkTime(logFor):
            messages.pop(0)  # remove the first message if needed
        else:
            break
    bot.serverMessages = messages


async def send(data, connection):
    ws = connection.ws
    sendEv = connection.sendEv
    await sendEv.trigger(ws.nurs, data, ws, blocking=True)
#    print(f'^  {data}')
    data = pack(data)
#    print(data)
    await ws.send_message(data)
    logger.info(f'sent {data}')


def getInfo(token):
    headers = {'authorization': f'Bearer {token}'}  # oauth header
    res = requests.get(me, headers=headers)
    json = res.json()
    if json['success']:
        return json['user']
    else:
        raise BaseException(json['errors'][0]['msg'])


def getRibbon(token):
    headers = {'authorization': f'Bearer {token}'}  # oauth header
    res = requests.get(ribbon, headers=headers)
    json = res.json()
    if json['success']:
        return json['endpoint']  # endpoint from the api
    else:
        raise BaseException(json['errors'][0]['msg'])


# connect ->  receiver()
#             heartbeat()
# connect to a websocket and start a reciver and a heartbeat proccess
class Connection:
    def __init__(self, bot, endpoint=None):
        self.bot = bot
        self.pending = {}  # pending messages
        self.ws = None
        self.endpoint = endpoint
        self.closed = False
        self.nurs = None

        # events
        sendEv = Event('sendEv', errorEvent=False)
        self.sendEv = sendEv
        conn = Event('conn', errorEvent=False)
        self.conn = conn
        # message event afetr sorting
        message = Event('message', errorEvent=False)
        self.message = message
        _message = Event('_message', errorEvent=False)  # message event
        self._message = _message

        # add event listeners

        _message.addListener(self.sortMessages)
        conn.addListener(self.reciver)
        sendEv.addListener(self.changeId)
        conn.addListener(self.heartbeat)
        message.addListener(self.msgHandle)

    async def send(self, data):
        await send(data, self)

    async def connect(self, nurs):
        await self._connect(nurs)
        await self.send(new)

    async def _connect(self, nurs, endpoint=None):
        self.closed = False
        token = self.bot.token
        ribbon = endpoint or getRibbon(token)
        ws = await connect_websocket_url(nurs, ribbon)  # connect to ribbon
        ws.nurs = nurs
        self.nurs = nurs
        ws.bot = self.bot
        self.ws = ws
        self.bot.connection = self
        self.endpoint = ribbon
        await self.conn.trigger(nurs, self.bot)

    async def close(self):
        if not self.closed:
            await self.ws.aclose()
            self.closed = True

    async def reciver(self, _bot):
        while not self.closed:
            ws = self.ws
            try:
                res = await ws.get_message()
    #            print(res)
            except ConnectionClosed:
                self.closed = True
                return
            res = unpack(res)
#            print(f'v  {res}')
            logger.info(f'recived {res}')
            await self._message.trigger(ws.nurs, ws, res)

    async def sortMessages(self, ws, res):
        if not isinstance(res, tuple):
            await self.message.trigger(ws.nurs, ws, res)
            return
        bot = ws.bot
        sid = bot.serverId
        msgId = res[0]
        if msgId == sid + 1:
            await self.message.trigger(ws.nurs, ws, res)
            msgId += 1
        else:
            self.pending[msgId] = res
        while (msg := self.pending.get(msgId)):
            await self.message.trigger(ws.nurs, ws, msg)
            del self.pending[msgId]
            msgId += 1

    async def reconnect(self, ws, sockid, resumeToken):
        await self.close()
        await self._connect(self.nurs, ws)
        await self.send(resume(sockid, resumeToken))  # resume message
        # hello message
        await self.send(hello([message.message for message in self.bot.messages]))

    async def changeId(self, msg, ws):
        if isinstance(msg, bytes):
            return
        if 'id' in msg:
            ws.bot.messageId += 1
            log(msg, ws)  # log the message

    async def heartbeat(self, bot):
        while not self.closed:
            await self.send(ping)
            # note the time for the last sent ping, used to calculate the ping when we recive a pong
            bot.lastPing = time.time()
            await trio.sleep(bot.pingInterval)

    async def msgHandle(self, ws, msg):
        bot = ws.bot
        if msg == b'\x0c':  # pong
            ping = time.time() - bot.lastPing  # calculate the time it took to recive a pong
            bot.ping = ping
            await bot._trigger('pinged', ping)
            return
        await msgHandle(ws, msg)
    #    print(msg)
