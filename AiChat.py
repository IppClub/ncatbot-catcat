from ncatbot.utils.logger import get_log
from ncatbot.core.message import GroupMessage
from ncatbot.utils.config import config

import asyncio
import os
import aiofiles

from .responses.CatCatRes import cat_cat_response

_log = get_log()

global_chat_histories = []


async def gene_response(api_key, msg: GroupMessage, cat_prompt):
    # Check if the group_id exists in global_chat_histories
    # 判断文件是否存在
    history_file = f"plugins/CatCat/logs/{msg.group_id}_history.log"
    # 使用上下文管理器处理文件操作
    try:
        async with aiofiles.open(history_file, "r", encoding="utf-8") as f:
            lines = await f.readlines()
            last_group_message_time = float(lines[-1].split()[0]) if lines else 0
    except FileNotFoundError:
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        async with aiofiles.open(history_file, "w", encoding="utf-8") as f:
            current_time = asyncio.get_event_loop().time()
            await f.write(f"{current_time} manager(10101): init catcat\n")
        last_group_message_time = 0

    force_reply = False
    text_content = ""
    for message in msg.message:
        if message["type"] == "text":
            text_content += (message["data"]["text"] + ",")
        if message["type"] == "at" and message["data"]["qq"] == config.bt_uin:
            text_content = f"@猫猫({config.bt_uin}) " + text_content
            force_reply = True

    text_content = f"{msg.sender.nickname}({msg.sender.user_id}): {text_content}"

    # Append the new message to the appropriate chat history
    with open(f"plugins/CatCat/logs/{msg.group_id}_history.log", "a", encoding="utf-8") as f:
        f.write(f"{asyncio.get_event_loop().time()} {text_content}\n")

    current_time = asyncio.get_event_loop().time()
    if current_time - last_group_message_time < 10 and not force_reply:
        return

    _log.info("开始生成回复……")
    with open(f"plugins/CatCat/logs/{msg.group_id}_history.log", "r", encoding="utf-8") as f:
        lines = f.readlines()
        chat_history = lines[-min(10, len(lines)):]
    response = await cat_cat_response(api_key, chat_history, cat_prompt)
    _log.info(f"猫猫：{response}")
    if response == "":
        return
    with open(f"plugins/CatCat/logs/{msg.group_id}_history.log", "a", encoding="utf-8") as f:
        f.write(f"{asyncio.get_event_loop().time()} 猫猫({config.bt_uin}): {response}\n")
    return response
