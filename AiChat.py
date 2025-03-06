from ncatbot.utils.logger import get_log
from ncatbot.core.message import GroupMessage
from ncatbot.utils.config import config

from collections import deque
import asyncio
from .responses.CatCatRes import cat_cat_response

_log = get_log()


async def gene_response(api_key, global_chat_histories, last_group_message_time, msg: GroupMessage, cat_prompt):
    # Check if the group_id exists in global_chat_histories
    if msg.group_id not in global_chat_histories:
        global_chat_histories[msg.group_id] = deque(maxlen=20)
    if msg.group_id not in last_group_message_time:
        last_group_message_time[msg.group_id] = -10

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
    global_chat_histories[msg.group_id].append(text_content)

    current_time = asyncio.get_event_loop().time()
    if current_time - last_group_message_time[msg.group_id] < 10 and not force_reply:
        return
    last_group_message_time[msg.group_id] = current_time

    with open(f"plugins/CatCat/logs/{msg.group_id}_history.log", "a", encoding="utf-8") as f:
        f.write(
            f"{asyncio.get_event_loop().time()}: Group {msg.group_id} - {list(global_chat_histories[msg.group_id])}\n")
    _log.info("开始生成回复……")
    response = await cat_cat_response(api_key, global_chat_histories[msg.group_id], cat_prompt)
    _log.info(f"猫猫：{response}")
    if response == "":
        return
    global_chat_histories[msg.group_id].append(f"猫猫({config.bt_uin}): {response}")
    return response
