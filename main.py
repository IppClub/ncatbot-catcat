# main.py

from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage
from ncatbot.utils.logger import get_log
from .AiChat import geneResponse
_log = get_log()
import yaml

bot = CompatibleEnrollment  # 兼容回调函数注册器

api_key = ""
cat_prompt = ""
manager_id = ""

class CatCat(BasePlugin):
    name = "CatCat" # 插件名称
    version = "1.0.3" # 插件版本

    @bot.group_event()
    async def on_group_event(self, msg: GroupMessage):
        # 定义的回调函数
        if msg.raw_message == "测试CatCat":
            await self.api.post_group_msg(msg.group_id, text="NCatBot插件CatCat测试成功喵")

    @bot.group_event()
    async def on_group_message(self, msg: GroupMessage):
        _log.info(f"{msg.sender.nickname}({msg.sender.user_id}): {msg.raw_message[:10]}")
        response = await geneResponse(api_key, msg, cat_prompt)
        await self.api.post_group_msg(msg.group_id, response)

    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):
        global cat_prompt
        if msg.user_id != manager_id:  # 修改判断条件
            return
        # 定义的回调函数
        if msg.raw_message == "prompt":
            await self.api.post_private_msg(msg.sender.user_id, text=cat_prompt)
        elif msg.raw_message[:10] == "set_prompt":
            cat_prompt = msg.raw_message[10:]
            with open("plugins/CatCat/config/cat_prompt.txt", "w", encoding="utf-8") as f:
                f.write(cat_prompt.strip())
            await self.api.post_private_msg(msg.sender.user_id, text="设置成功")


    async def on_load(self):
        print("插件加载中……")
        # 从 config/config.yaml 中读取配置
        with open("plugins/CatCat/config/config.yaml", "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            global api_key
            api_key = config_data["api_key"]
            global manager_id
            manager_id = config_data["manager_id"]

        with open("plugins/CatCat/config/cat_prompt.txt", "r", encoding="utf-8") as f:
            global cat_prompt
            cat_prompt = f.read()
        # 插件加载时执行的操作, 可缺省
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")
