from typing import Dict, List

from app.agent_router import detect_intent
from app.agent_tools import tool_rag_answer, tool_reading_card, tool_compare_papers
from app.qwen_api import qwen_chat


def run_chat_round(messages: List[Dict]) -> Dict:
    """
    接收对话历史 messages（[{role, content}...]），执行一轮推理并返回 assistant 消息。
    路由至工具或直接闲聊。
    """
    user_msg = None
    for m in reversed(messages):
        if m.get("role") == "user":
            user_msg = m.get("content")
            break
    if not user_msg:
        return {"role": "assistant", "content": "请先输入你的问题。"}

    intent, args = detect_intent(user_msg)

    if intent == "reading_card":
        res = tool_reading_card(args["query"])
        data = res["data"]
        content = "[工作流: 速读卡]\n\n" + data.get("card", "")
        return {"role": "assistant", "content": content}

    if intent == "compare_papers":
        res = tool_compare_papers(args.get("topic", user_msg), picks=args.get("picks"))
        data = res["data"]
        content = "[工作流: 论文对比]\n\n" + data.get("table", "")
        return {"role": "assistant", "content": content}

    if intent == "rag_answer":
        res = tool_rag_answer(args["query"])
        data = res["data"]
        answer = data.get("answer", "")
        return {"role": "assistant", "content": "[工作流: 知识库问答]\n\n" + answer}

    if intent == "run_eval":
        return {"role": "assistant", "content": "评估工作流已在评估页提供，一键运行即可。"}

    # chat_free：使用简短 system 保障风格
    system = (
        "你是一个友好且克制的助理，名字为 ResearchAgent。"
        "默认身份是‘论文与项目知识库助手’，可以调用速读卡/论文对比/知识库问答等工作流。"
        "回答要简洁；涉及事实时建议说明依据或提示用户去‘速读卡/对比’模式获取引用。"
    )
    reply = qwen_chat(system_prompt=system, user_prompt=user_msg)
    return {"role": "assistant", "content": reply}


