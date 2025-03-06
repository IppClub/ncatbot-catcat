# main.py

from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage
from ncatbot.utils.config import config
import asyncio
from ncatbot.utils.logger import get_log
_log = get_log()
from .responses.CatCatRes import dora_ssr_response
import yaml

bot = CompatibleEnrollment  # 兼容回调函数注册器


global_chat_histories = {}

last_group_message_time = {}

api_key = ""
cat_prompt = ""

class CatCat(BasePlugin):
    name = "CatCat" # 插件名称
    version = "1.0.0" # 插件版本

    @bot.group_event()
    async def on_group_event(self, msg: GroupMessage):
        # 定义的回调函数
        if msg.raw_message == "测试CatCat":
            await self.api.post_group_msg(msg.group_id, text="Ncatbot插件CatCat测试成功喵")

    @bot.group_event()
    async def on_group_message(self, msg: GroupMessage):
        global last_group_message_time, global_chat_histories

        # Check if the group_id exists in global_chat_histories
        if msg.group_id not in global_chat_histories:
            global_chat_histories[msg.group_id] = []
        if msg.group_id not in last_group_message_time:
            last_group_message_time[msg.group_id] = -10

        
        force_reply = False
        text_content = {"user": msg.sender.nickname, "text": ""}
        
        for message in msg.message:
            if message["type"] == "text":
                text_content["text"] += message["data"]["text"]
            if message["type"] == "at" and message["data"]["qq"] == config.bt_uin:
                text_content["text"] += "@猫猫"
                force_reply = True

        # Append the new message to the appropriate chat history
        chat_history = global_chat_histories[msg.group_id]
        chat_history.append(text_content)
        
        current_time = asyncio.get_event_loop().time()
        if current_time - last_group_message_time[msg.group_id] < 10 and not force_reply:
            return
        last_group_message_time[msg.group_id] = current_time

        

        _log.info(f"最近一条群聊记录：{chat_history[-1]}")
        _log.info("开始生成回复……")
        response = dora_ssr_response(api_key, chat_history[-20:], cat_prompt)
        _log.info(f"猫猫：{response}")
        if response == "":
            return
        chat_history.append({"user": "猫猫", "text": response})
        await self.api.post_group_msg(msg.group_id, response)



    async def on_load(self):
        print("插件加载中……")
        # 从 config/config.yaml 中读取配置
        with open("plugins/CatCat/config/config.yaml", "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            global api_key
            api_key = config_data["api_key"]

        with open("plugins/CatCat/config/cat_prompt.txt", "r", encoding="utf-8") as f:
            global cat_prompt
            cat_prompt = f.read()
        # 插件加载时执行的操作, 可缺省
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")
