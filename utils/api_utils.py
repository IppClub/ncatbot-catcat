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
        "temperature": 1.3,
        "max_tokens": 256,
    }

    try:
        async with aiohttp.ClientSession() as session:
            # log messages file
            with open("plugins/CatCat/logs/deepseek_api/messages.log", "w", encoding="utf-8") as f:
                f.write(f"{{ {messages} }}\n")
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    try:
                        return result['choices'][0]['message']['content']
                    except KeyError:
                        raise KeyError(f"提取回复时出错，回复内容：{result}")
                else:
                    error_text = await response.text()
                    _log.error(f"API调用失败：状态码 {response.status}，响应内容：{error_text}")
    except aiohttp.ClientError as e:
        _log.error(f"网络请求出错：{str(e)}")
    except Exception as e:
        _log.error(f"未知错误：{str(e)}")