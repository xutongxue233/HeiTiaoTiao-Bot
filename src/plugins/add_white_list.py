import yaml
import os
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin.on import on_command

# 设置白名单文件路径
WHITE_LIST_FILE = "./config/white_list.yml"

# 如果白名单文件不存在，初始化文件内容
if not os.path.exists(WHITE_LIST_FILE):
    with open(WHITE_LIST_FILE, 'w', encoding='utf-8') as f:
        yaml.dump({"group": [], "friend": []}, f, allow_unicode=True)


# 读取白名单
def load_white_list():
    with open(WHITE_LIST_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# 写入白名单
def save_white_list(white_list):
    with open(WHITE_LIST_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(white_list, f, allow_unicode=True)


add_qq_white = on_command("qqwhite", aliases={"加Q白"}, permission=SUPERUSER)
add_group_white = on_command("groupwhite", aliases={"加群白"}, permission=SUPERUSER)


@add_qq_white.handle()
async def _(args: Message = CommandArg()):
    # 获取白名单数据
    white_list = load_white_list()

    # 获取传入的QQ号并检查是否已存在
    qq = args.extract_plain_text()
    if qq in white_list["friend"]:
        await add_qq_white.finish(f"QQ:{qq} 已经在白名单中")
    else:
        white_list["friend"].append(qq)
        save_white_list(white_list)  # 保存更新后的白名单
        await add_qq_white.finish(f"QQ:{qq} 已成功添加到白名单")


@add_group_white.handle()
async def _(args: Message = CommandArg()):
    # 获取白名单数据
    white_list = load_white_list()

    # 获取传入的群号并检查是否已存在
    group = args.extract_plain_text()
    if group in white_list["group"]:
        await add_group_white.finish(f"群:{group} 已经在白名单中")
    else:
        white_list["group"].append(group)
        save_white_list(white_list)  # 保存更新后的白名单
        await add_group_white.finish(f"群:{group} 已成功添加到白名单")
