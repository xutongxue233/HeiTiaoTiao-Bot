from nonebot.adapters.onebot.v11 import Bot, GroupRequestEvent
from nonebot.plugin.on import on_request

add_group = on_request()

@add_group.handle()
async def _(bot: Bot, event: GroupRequestEvent):
    if event.request_type == 'group':
        await event.approve(bot)