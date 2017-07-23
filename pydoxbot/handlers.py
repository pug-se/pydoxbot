"""
Bot message handlers.
"""
from typing import Dict

import pydoc
import telepot


def _build_article(query: str) -> Dict[str, str]:
    article = {'type': 'article', 'id': 'abc'}
    article['title'] = query
    doc = pydoc.render_doc(query, renderer=pydoc.plaintext)
    article['message_text'] = doc[:4095] if len(doc) > 4096 else doc
    article['description'] = doc.split('\n', maxsplit=1)[0]
    return article


def inline_handler(bot):
    """
    Handle inline queries
    """
    async def on_inline_query(msg: str):
        query_id, _, query_string = telepot.glance(msg, flavor='inline_query')
        if query_string:
            try:
                await bot.answerInlineQuery(query_id, [_build_article(query_string)])
            except ImportError:
                pass
    return on_inline_query
