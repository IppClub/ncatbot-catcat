from ..AiChat import call_deepseek_chat_api,format_group_chat  

async def dora_ssr_response(api_key, chat_history, prompt):
	"""
	参数：
		chat_history: 原始群聊记录（包含用户和文本的字典列表）
	"""
	messages = [
		{"role": "system", "content": prompt},
		*format_group_chat(chat_history),
		{"role": "user", "content": "请根据上述规则判断是否需要回复，并严格按格式输出："}
	]

	response = await call_deepseek_chat_api(api_key, messages)

	# 清洗可能出现的额外符号
	return response.strip('"') if response else ""