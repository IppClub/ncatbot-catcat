from ncatbot.utils.logger import get_log
import aiohttp

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
                    return
    except Exception as e:
        _log.error(f"API调用出错：{str(e)}")
        return
