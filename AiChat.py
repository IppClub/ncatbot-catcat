from ncatbot.utils.logger import get_log
import requests
_log = get_log()


def call_deepseek_chat_api(api_key, messages):
	"""
	调用 DeepSeek Chat API
	参数：
		api_key: 你的 API 密钥
		messages: 对话消息列表，格式示例：
			[
				{"role": "user", "content": "你好"},
				{"role": "assistant", "content": "你好！有什么可以帮助你的？"},
				{"role": "user", "content": "请介绍下上海"}
			]
	"""
	url = "https://api.deepseek.com/chat/completions"

	headers = {
		"Content-Type": "application/json",
		"Accept": "application/json",
		"Authorization": f"Bearer {api_key}"
	}

	data = {
		"model": "deepseek-chat", # 根据需要选择模型
		"messages": messages,
		"temperature": 0.3,
		"max_tokens": 256,
	}

	try:
		response = requests.post(url, headers=headers, json=data)
		response.raise_for_status()  # 检查 HTTP 错误
		result = response.json()

		if "choices" in result:
			return result["choices"][0]["message"]["content"]
		else:
			_log.info("未收到有效响应")
			return ""

	except requests.exceptions.RequestException as e:
		_log.info(f"请求异常：{str(e)}")
		return ""
	except Exception as e:
		_log.info(f"处理响应时发生错误：{str(e)}")
		return ""


def format_group_chat(messages):
	"""
	将原始群聊记录转换为 API 接受的格式
	输入示例：
		[
			{"user": "开发者A", "text": "Dora SSR 的物理系统怎么优化？"},
			{"user": "开发者B", "text": "试试看文档第三章的示例代码"}
		]
	"""
	return [
		{"role": "user", "content": f"{msg['user']}：{msg['text']}"}
		for msg in messages
	]