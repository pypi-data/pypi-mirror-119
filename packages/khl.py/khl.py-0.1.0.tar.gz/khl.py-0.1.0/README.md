[> 加入我们的 khl 服务器 | Join our server on khl](https://kaihei.co/JJE0Es)

# special notes for v0.1.0

**v0.1.0 is a breaking version** with better architecture, simpler API, more powerful components etc.

if you do not want to migrate existing code, please stay at v0.0.10

by the way, have a try on v0.1.0 is a piece of cake, and we wanna your feedback or help(if you are willing to)

# khl.py

Python SDK for [kaiheila.cn](https://www.kaiheila.cn/) API

# install

Python requirement: >= Python 3.6

```shell
pip install khl.py
```

# quickly enroll

Minimal example:

```python
from khl import Bot, Message

# init Bot
bot = Bot(token='xxxxxxxxxxxxxxxxxxxxxxxxx')


# register command
# invoke this via saying `/hello` in channel
@bot.command(name='hello')
async def world(msg: Message):
    await msg.reply('world!')


# everything done, go ahead now!
bot.run()
# now invite the bot to a server, and type '/hello'(in any channel)
# (remember to grant the bot with read & send permissions)
```

For more example and tutorial, please turn to [example](./example)

## notes for Mac OSX users:

if you encounter this error:

```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1123)
```

please install certificate manually, turning to this post for guide:

[certificate verify failed: unable to get local issuer certificate](https://stackoverflow.com/a/58525755)

# short-term roadmap

## feat

- bot.on_event()
- helper function for apis

# commit message rules

only accept commits satisfying [Conventional Commits convention](https://github.com/commitizen/cz-cli)

search plugins with keyword `commitizen` for your editor/IDE, then addict to write commit message
