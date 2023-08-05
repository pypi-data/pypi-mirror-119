# discord-surveys
A survey object that utilizes discord.py and discord-interactions.
## Examples

### Discord

![Example](https://i.imgur.com/7zqcdOz.png)

![Example](https://i.imgur.com/ql2lcKg.png)

### Python
```py
from discord_surveys import Survey

async def survey(self, ctx: SlashContext, question: str, options: str):
    await Survey(
        bot=ctx.bot,
        ctx=ctx,
        question=question,
        options=options
    ).send()
```

## Description

Attributes | Description
---|---
`bot` | `discord.Bot` or `discord.AutoShardedBot`
`ctx` | `discord_slash.context.SlashContext`
`embed` | `discord.Embed`
`options` | `str` and then converted to `SurveyOption`.
`timeout` | (Optional) `int`


