# main.py

from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage
from ncatbot.utils.logger import get_log

from .AiChat import gene_response

import yaml

_log = get_log()

bot = CompatibleEnrollment  # 兼容回调函数注册器

global_chat_histories = {}
last_group_message_time = {}

api_key = ""
cat_prompt = ""


class CatCat(BasePlugin):
    name = "CatCat"  # 插件名称
    version = "1.0.2"  # 插件版本

    @bot.group_event()
    async def on_group_event(self, msg: GroupMessage):
        # 定义的回调函数
        if msg.raw_message == "测试CatCat":
            await self.api.post_group_msg(msg.group_id, text="NCatBot插件CatCat测试成功喵")

    @bot.group_event()
    async def on_group_message(self, msg: GroupMessage):
        global last_group_message_time, global_chat_histories
        response = await gene_response(api_key, global_chat_histories, last_group_message_time, msg, cat_prompt)
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
