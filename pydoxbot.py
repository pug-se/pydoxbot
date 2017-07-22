"""
Python documentation inline bot.
"""

import asyncio
import os
import pydoc

import telepot
import telepot.aio
import telepot.aio.loop
import aiohttp.web as web


TOKEN = os.environ['BOT_API_TOKEN']
URL = os.environ['BOT_SERVER_URL']
PORT = int(os.environ['PORT'])


def create_result(query):
    article = {'type': 'article', 'id': 'abc'}
    article['title'] = query
    doc = pydoc.render_doc(query, renderer=pydoc.plaintext)
    article['message_text'] = doc[:4095] if len(doc) > 4096 else doc
    article['description'] = doc.split('\n', maxsplit=1)[0]
    return article


def inline_handler(bot):
    async def on_inline_query(msg):
        query_id, _, query_string = telepot.glance(msg, flavor='inline_query')
        if query_string:
            try:
                await bot.answerInlineQuery(query_id, [create_result(query_string)])
            except ImportError:
                pass
    return on_inline_query


async def server_init(app, bot, webhook):
    async def bot_feeder(request):
        data = await request.text()
        webhook.feed(data)
        return web.Response(body='OK'.encode('utf-8'))

    app.router.add_route('GET', f'/{TOKEN}', bot_feeder)
    app.router.add_route('POST', f'/{TOKEN}', bot_feeder)

    await bot.setWebhook(f'https://{URL}/{TOKEN}')


def run():
    loop = asyncio.get_event_loop()

    app = web.Application(loop=loop)
    bot = telepot.aio.Bot(TOKEN, loop=loop)
    webhook = telepot.aio.loop.OrderedWebhook(bot, {'inline_query': inline_handler(bot)})

    loop.run_until_complete(server_init(app, bot, webhook))
    loop.create_task(webhook.run_forever())

    try:
        web.run_app(app, port=PORT)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
