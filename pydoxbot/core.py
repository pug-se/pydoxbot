"""
Bootstraps the bot's message pooling or webhook.
"""

import asyncio
import os

import telepot.aio
import telepot.aio.loop
import aiohttp.web as web

import handlers


TOKEN = os.environ['BOT_API_TOKEN']
URL = os.environ.get('BOT_SERVER_URL')
PORT = os.environ.get('PORT')


async def server_init(app, bot, webhook):
    async def bot_feeder(request):
        data = await request.text()
        webhook.feed(data)
        return web.Response(body='OK'.encode('utf-8'))

    app.router.add_route('GET', f'/{TOKEN}', bot_feeder)
    app.router.add_route('POST', f'/{TOKEN}', bot_feeder)

    await bot.setWebhook(f'https://{URL}/{TOKEN}')


def run_as_weebook(loop, bot):
    app = web.Application(loop=loop)
    webhook = telepot.aio.loop.OrderedWebhook(bot, {'inline_query': handlers.inline_handler(bot)})

    loop.run_until_complete(server_init(app, bot, webhook))
    loop.create_task(webhook.run_forever())

    try:
        web.run_app(app, port=int(PORT))
    except KeyboardInterrupt:
        pass


def run_as_pooling(loop, bot):
    pool = telepot.aio.loop.MessageLoop(bot, {'inline_query': handlers.inline_handler(bot)})

    async def delete_webhook(bot):
        await bot.setWebhook()

    loop.run_until_complete(delete_webhook(bot))
    loop.create_task(pool.run_forever())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

def bootstrap():
    loop = asyncio.get_event_loop()
    bot = telepot.aio.Bot(TOKEN, loop=loop)

    if URL and PORT:
        run_as_weebook(loop, bot)
    else:
        run_as_pooling(loop, bot)

if __name__ == '__main__':
    bootstrap()
