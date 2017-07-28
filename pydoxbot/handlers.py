"""
Bot message handlers.
"""
from typing import Dict, List
from asyncio import CancelledError, InvalidStateError

import telepot

import docs

_MESSAGE_SIZE_LIMIT = 4096 # Telegram's character limit for bot messages
_NOT_FOUND_PARAMS = {
    'switch_pm_text': 'No docs found. Tap for Help.',
    'switch_pm_parameter': 'Help'
}


def _create_article(title, desc, text, article_id='0'):
    article = {'type': 'article'}
    article['id'] = article_id
    article['title'] = title
    article['description'] = desc
    article['message_text'] = text[:_MESSAGE_SIZE_LIMIT]
    return article


def _build_articles(query: str) -> List[Dict[str, str]]:
    return [_create_article(title, subtitle, text) for title, subtitle, text in docs.find(query)]


def inline_handler(bot):
    """
    Handle inline queries
    """
    async def on_inline_query(msg: str):
        query_id, _, query_string = telepot.glance(msg, flavor='inline_query')
        if query_string:
            try:
                articles = _build_articles(query_string)
                if articles:
                    await bot.answerInlineQuery(query_id, articles)
                else:
                    await bot.answerInlineQuery(query_id, articles, **_NOT_FOUND_PARAMS)
            except (CancelledError, InvalidStateError):
                pass # Should log the error
    return on_inline_query
