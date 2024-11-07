from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Message, Event, Bot
from nonebot.params import CommandArg
import random

from src.util.ehentai_utils import ehentai_utils
from src.util.ehentai_utils import ehentai_download

ehentai = on_command("ehentai", aliases={"今日新本", "随机本子"})

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
    # 定义最大获取条目数
    max_results = 5
    max_page_count = 30

    # 获取最多 5 个搜索结果
    results = ehentai_utils.get_ehentai_list(max_results=max_results)

    # 过滤出页数小于 max_page_count 的结果
    filtered_results = [result for result in results if int(result['pages']) < max_page_count]

    # 如果没有找到符合条件的图集，增加爬取数量
    while not filtered_results:
        max_results += 5  # 增加搜索条目数
        results = ehentai_utils.get_ehentai_list(max_results=max_results)
        filtered_results = [result for result in results if int(result['pages']) < max_page_count]
        if max_results > 40:  # 防止死循环，设置最大爬取限制
            break

    if filtered_results:
        # 获取页数最少的结果
        result = min(filtered_results, key=lambda x: x['pages'])  # 根据 pages 选择最小的条目
        print(f"随机下载本子页数: {result['pages']}")

        # 下载该条目的图片并生成 PDF
        try:
            pdf_file = ehentai_download.download_images_and_create_pdf(result['href'], int(result['pages']))
            # 发送消息：说明文件已下载
            await ehentai_down.send("已下载图集，正在发送 PDF...")
            await bot.call_api(
                'upload_group_file',  # API 名称
                group_id=group_id,  # 群聊ID
                file=pdf_file  # 文件路径
            )
        except Exception as e:
            await ehentai_down.send(f"下载或发送 PDF 时发生错误：{str(e)}")  # 直接发送字符串
    else:
        # 如果没有找到符合条件的图集
        await ehentai_down.send("未找到符合条件的图集，页数必须小于 30。")

