from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Message, Event, Bot
from nonebot.params import CommandArg
import random

from src.util.ehentai_utils import ehentai_utils
from src.util.ehentai_utils import ehentai_download

ehentai = on_command("ehentai", aliases={"每日一本", "随机本子"})

ehentai_down = on_command("ehentai_download", aliases={"随机下载本子"})

@ehentai.handle()
async def _(args: Message = CommandArg()):
    results = ehentai_utils.get_ehentai_list(max_results=3)
    length = len(results)
    # 随机获取其中一个
    result = results[random.randint(0, length - 1)]
    # 创建消息内容
    message = f"标题：{result['title']}\n"

    # 如果有图片链接，添加图片
    if result['image_url']:
        message += MessageSegment.image(result['image_url'])

    await ehentai.finish(Message(message))


@ehentai_down.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    group_id = event.group_id
    # 定义最大获取条目数和目标页数
    max_results = 10
    max_page_count = 35  # 目标：页数小于35的图集
    limit_result = 50

    while True:
        results = ehentai_utils.get_ehentai_list(max_results=max_results)
        # 筛选出页数小于 max_page_count 的图集
        filtered_results = [result for result in results if int(result['pages']) < max_page_count]
        if filtered_results or max_results >= limit_result:  # 找到符合条件的图集，或爬取数量达到上限
            break
        max_results += 5  # 如果没找到，增加搜索条目数

    if filtered_results:
        result = filtered_results[0]  # 直接取第一个符合条件的图集
        print(f"下载图集，页数: {result['pages']}")  # 输出图集页数
        try:
            # 获取长图路径
            long_image_path = ehentai_download.download_images_and_create_long_image(result['href'], int(result['pages']), max_threads=5)
            # 发送消息：文件下载完成
            await ehentai_down.send("已下载图集，正在发送长图....")
            # 上传长图文件到群聊
            await bot.call_api(
                'upload_group_file',
                group_id=group_id,
                file=long_image_path
            )
        except Exception as e:
            await ehentai_down.send(f"下载或发送失败：{str(e)}")
    else:
        # 没有找到符合条件的图集
        await ehentai_down.send(f"未找到符合条件的图集，页数必须小于 {max_page_count}。")


