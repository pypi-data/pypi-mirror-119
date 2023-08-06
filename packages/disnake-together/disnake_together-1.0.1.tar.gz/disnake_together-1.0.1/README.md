# disnake-together

## Table of Contents

- [About](#about)
- [Examples](#examples)
- [prerequisites](#prerequisites)
- [Contributing](#contributing)

## About <a name = "about"></a>

A 3rd party library for Discord's BETA feature of VC Party Games
<br>


### Prerequisites

You should have disnake installed in order to use this package
<br>
To install disnake, run the following code in a terminal
```
pip install disnake
```

### Examples <a name = "examples"></a>

Generate a link for YouTube Together

```py
from disnake.ext import commands
from disnake_together import DisnakeTogether
    
client = commands.Bot(command_prefix="*")

@client.command()
async def youtube_together(self, ctx):
    together_control = DiscordTogether(self.client)
    # To check if the user is in a vc
    try:
        vc = ctx.author.voice.channel.id
    except Exception as _:
        await ctx.channel.send("You are not in a VC, please join one and then use the command")
    # Get invite link
    link = await together_control.create_link(vc, 'youtube')
    await ctx.send(f"Click the link 👇\n{link}")

```

You can replace `youtube` with the other interactions i.e betrayal, chess, fishing, poker

### Contributing <a name = "contributing"></a>
- [LamerGamerYT](https://github.com/lamergameryt)
- [Bxllistic](https://github.com/apurv-r)
