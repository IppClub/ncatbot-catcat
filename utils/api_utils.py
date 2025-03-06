import aiohttp
from ncatbot.utils.logger import get_log

_log = get_log()

async def call_deepseek_chat_api(api_key, messages):
    url = "https://api.deepseek.com/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 256,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                else:
                    _log.error(f"API调用失败：{response.status}")
                    return None
    except Exception as e:
        _log.error(f"API调用出错：{str(e)}")
        return None

def format_group_chat(messages):
	"""
	将原始群聊记录转换为 API 接受的格式
	输入示例：
		[
			"开发者A(123456): 系统怎么优化?",
			"开发者B(987654): 试试看文档第三章的示例代码"
		]
	"""
	formatted_messages = ""
	for message in messages:
		formatted_messages += f"{message}\n"
	return [
		{"role": "user", "content": formatted_messages}
  ]