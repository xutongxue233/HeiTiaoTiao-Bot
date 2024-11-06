from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.params import CommandArg
import random
from src.util.ehentai_utils import ehentai_utils

ehentai = on_command("ehentai", aliases={"今日新本", "随机本子"})


@ehentai.handle()
async def _(args: Message = CommandArg()):
    results = ehentai_utils.get_ehentai_list()
    length = len(results)
    # 随机获取其中一个
    result = results[random.randint(0, length - 1)]
    print(result)
    # 创建消息内容
    message = f"标题：{result['title']}\n"

    # 如果有图片链接，添加图片
    if result['image_url']:
        message += MessageSegment.image(result['image_url'])

    await ehentai.finish(Message(message))
