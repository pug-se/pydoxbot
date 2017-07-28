"""
Docs access helpers.
"""
import pydoc


def find(query):
    try:
        docstring = pydoc.render_doc(query, renderer=pydoc.plaintext)
        title = query
        subtitle = docstring.split(sep='\n', maxsplit=1)[0]
        message = docstring
        yield title, subtitle, message
    except ImportError:
        pass
