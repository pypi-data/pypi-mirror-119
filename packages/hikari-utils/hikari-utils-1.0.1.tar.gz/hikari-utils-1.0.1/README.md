# hikari-utils
A python package with utils for hikari

# THIS PROJECT IS STILL IN EARLY STAGES!
This project is still in early development and we will keep adding features

# Samples
## Lightbulb Bot
```python
import hutils
import hikari

bot = hutils.lightbulbbot(token="Discord Bot Token", prefix="Discord Bot Prefix", intents=hikari.Intents.ALL, insensitive=True)

bot.run()
```
## Tanjun Bot
```python
import hutils
import hikari

bot = hutils.tanjunbot(token="Discord Bot Token", guild_id=Discord Bot Guild ID, module_path="./modules")

bot.run()
```

# Note:
When you invite your bot to your server, please add the ```applications.commands``` when generating the invite link, otherwise your bot won't work.