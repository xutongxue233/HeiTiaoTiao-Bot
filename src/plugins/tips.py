
from nonebot import require, get_bot
from nonebot.adapters.onebot.v11 import Bot, MessageSegment

# 获取 apscheduler 插件
timing = require("nonebot_plugin_apscheduler").scheduler

@timing.scheduled_job("cron", hour='11', minute='35', id="send_color")
async def send_color():
    bot: Bot = get_bot()
    # 构建 @ 指定 QQ 号的消息
    message = MessageSegment.at(895945745) + " 该发色图了！"
    # 发送消息到指定群聊
    await bot.send_group_msg(group_id=735944570, message=message)


#提醒喝水机器人
@timing.scheduled_job("cron", hour='8-23', minute='30', id="drink_water")
async def drink_water():
    bot: Bot = get_bot()
    # 构建 @ 指定 QQ 号的消息
    message = MessageSegment.at(895945745) + " 该喝水了喵~"
    # 发送消息到指定群聊
    await bot.send_group_msg(group_id=735944570, message=message)
