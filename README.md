# PyDoxBot (alpha)
Your companion bot for referring the python documentation.

## Usage


Requirements:
- Python 3.6+
- [Telepot](https://github.com/nickoala/telepot/) - framework for telegram bot api
- [aiohttp](http://aiohttp.readthedocs.io/en/stable/) - asynchronous HTTP Client/Server


### Setup your enviroment:

```shell
$ pyenv virtualenv 3.6.0 pydoxbot
$ pyenv activate pydoxbot
(pydoxbot) $
```
> *Using pyenv and virtualenv is not a requirement, however, I highly recommend its usage for manage python and packages' versions.*


### Install dependencies:

```shell
$ pip install -r requirements.txt
```

### Export environment variables:

```
$ export BOT_API_TOKEN=<your telegram bot token here>
```

> **For production only**:
> 
> When running in production Telegram recommends that you use a webhook approach. It has [some advantages](https://core.telegram.org/bots/webhooks) over the long pooling one.
> ```
> $ export BOT_SERVER_URL=<bot host public url>
> $ export PORT=<port number>
> ```

### Running the bot

```
$ python pydoxbot/core.py
```