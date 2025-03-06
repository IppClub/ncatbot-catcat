from ..utils.api_utils import call_deepseek_chat_api


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


async def cat_cat_response(api_key, chat_history, prompt):
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
