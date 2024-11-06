from nonebot import on_request
from nonebot.adapters.onebot.v11 import FriendRequestEvent, Bot

add_friend = on_request()


@add_friend.handle()
async def _(bot: Bot, event: FriendRequestEvent):
    # 检查请求类型是否为好友请求
    if event.request_type == "friend":
        # 自动同意好友请求
        await event.approve(bot)
