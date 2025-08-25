import os
from typing import Optional


def qwen_chat(system_prompt: str, user_prompt: str, model: Optional[str] = None, temperature: Optional[float] = None) -> str:
    """
    简化的 Qwen Chat API 封装。

    为了便于快速搭建MVP，这里默认从环境变量中读取阿里云 DashScope Key：DASHSCOPE_API_KEY。
    若没有配置，也可以退化到本地简单“模板”回复，保证页面可跑通。
    """
    try:
        import dashscope
        from httpx import TimeoutException
    except Exception:
        dashscope = None

    try:
        from openai import OpenAI as OpenAIClient
    except Exception:
        OpenAIClient = None

    # 优先环境变量，其次尝试本地配置文件 app/config_local.py
    api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        try:
            from . import config_local  # python -m 方式
        except Exception:
            try:
                import config_local  # 直接运行方式
            except Exception:
                config_local = None
        if config_local is not None:
            api_key = getattr(config_local, "DASHSCOPE_API_KEY", "").strip()
    if dashscope is None or not api_key:
        # 兜底：无 Key 或未安装 dashscope，则返回模板回答
        return (
            "[本地占位回答] 未检测到 DashScope 配置，将基于检索到的资料给出简要回答.\n"
            f"System: {system_prompt[:60]}...\nUser: {user_prompt[:200]}...\n"
            "请在本机设置环境变量 DASHSCOPE_API_KEY，并安装 dashscope 以启用真实调用。"
        )

    dashscope.api_key = api_key
    # 使用兼容性更好的默认模型名
    # 读取模型名：环境变量优先，其次本地配置
    model_name = model or os.getenv("QWEN_MODEL", "").strip()
    if not model_name:
        try:
            from . import config_local as _cfg1
            model_name = getattr(_cfg1, "QWEN_MODEL", "").strip()
        except Exception:
            try:
                import config_local as _cfg2
                model_name = getattr(_cfg2, "QWEN_MODEL", "").strip()
            except Exception:
                model_name = "qwen-turbo"

    # 构造对话
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # 优先使用 OpenAI 兼容模式（更稳定，与你粘贴的示例一致）
    if OpenAIClient is not None:
        try:
            client = OpenAIClient(
                api_key=api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
            kwargs = {"model": model_name, "messages": messages}
            if temperature is not None:
                kwargs["temperature"] = float(temperature)
            resp = client.chat.completions.create(**kwargs)
            if getattr(resp, "choices", None):
                return (resp.choices[0].message.content or "").strip()
        except Exception:
            pass

    # 使用 dashscope SDK，先尝试 messages，再尝试 prompt
    prompt_text = f"[System]\n{system_prompt}\n\n[User]\n{user_prompt}"

    try:
        # 先 messages 格式
        params = {}
        if temperature is not None:
            params["temperature"] = float(temperature)
        response = dashscope.Generation.call(
            model=model_name,
            input={"messages": messages},
            result_format="message",
            parameters=params if params else None,
        )
        if hasattr(response, "output") and response.output:
            choices = response.output.get("choices") or []
            if choices:
                return choices[0].get("message", {}).get("content", "") or ""
    except Exception:
        pass

    try:
        # 再 prompt 顶层参数
        params = {}
        if temperature is not None:
            params["temperature"] = float(temperature)
        response = dashscope.Generation.call(
            model=model_name,
            prompt=prompt_text,
            parameters=params if params else None,
        )
        if hasattr(response, "output_text") and isinstance(response.output_text, str):
            return response.output_text
        if hasattr(response, "output") and response.output:
            output = response.output
            if isinstance(output, dict):
                if "text" in output and isinstance(output["text"], str):
                    return output["text"]
                choices = output.get("choices") or []
                if choices:
                    return choices[0].get("message", {}).get("content", "") or ""
    except Exception:
        pass

    return "抱歉，未能从 Qwen 获得有效回复。"

