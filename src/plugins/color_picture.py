from nonebot import on_command
import httpx
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.params import CommandArg

cpic = on_command("cpic", aliases={"来点色图", "来点涩图"})


@cpic.handle()
async def _(args: Message = CommandArg()):
    tags = []
    if args.extract_plain_text() == "":
        tags = []
    else:
        tags = args.extract_plain_text().split(",")
    # 请求图片接口
    async with httpx.AsyncClient() as client:
        # 构建请求参数
        params = {
            # 0-关闭 1开启 2-混合
            "r18": 1,
            # 图片关键词
            # "keyword": args,
            # 图片标签
            "tag": tags,
            # 是否排除AI图
            "excludeAI": True
        }

        response = await client.post("https://api.lolicon.app/setu/v2", params=params)
        data = response.json()
    # 从返回数据中提取图片 URL
    if data.get("data"):
        img_url = data["data"][0]["urls"]["original"]
        await cpic.finish(MessageSegment.image(img_url))
    else:
        await cpic.finish("无法获取图片，请稍后再试。")
