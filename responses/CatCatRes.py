from ..utils.api_utils import call_deepseek_chat_api


def format_group_chat(messages):
    """
    将原始群聊记录转换为 API 接受的格式
    输入示例：
        [
            166658.6419105 manager(10101): init catcat
            166658.6430702 何山(7894652): @猫猫 你是谁,
        ]
    """
    formatted_messages = ""
    for message in messages:
        formatted_messages += f"{' '.join(message.split()[1:])}\n"
    # print(formatted_messages)
    return [{"role": "user", "content": formatted_messages}]


async def cat_cat_response(api_key, chat_history, prompt):
    """
    参数：
        chat_history: 群聊记录，格式为：
            [
                166658.6419105 manager(10101): init catcat
                166658.6430702 何山(98645135): @猫猫 你是谁,
            ]
    """
    try:
        messages = [
            {"role": "system", "content": prompt},
            *format_group_chat(chat_history),
            {"role": "user", "content": "请根据上述规则判断是否需要回复，并严格按格式输出："}
        ]

        response = await call_deepseek_chat_api(api_key, messages)
        return response.strip('"') if response else ""
    except Exception as e:
        print(f"CatCat响应生成错误: {str(e)}")
