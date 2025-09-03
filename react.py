# react_agent_weather.py

from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from langchain_core.tools import tool
from llm_utils import llm

# ======================
# 1. 定义工具（天气查询）
# ======================

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气（模拟）"""
    weather_data = {
        "北京": "晴，25°C，空气质量良好",
        "上海": "多云，28°C，湿度较高",
        "广州": "雷阵雨，30°C，注意防暑",
        "深圳": "暴雨，29°C，建议居家"
    }
    return weather_data.get(city, f"{city} 天气数据暂无")

tools = [get_weather]

# ⚡️ 一行代码创建 Agent！
graph = create_react_agent(
    model=llm,
    tools=tools,
    state_schema=AgentState  # 使用包含 remaining_steps 的 AgentState
)


if __name__ == "__main__":
    print("🌤️ 欢迎使用 ReAct 天气助手！输入 'quit' 退出\n")

    # 可以支持多轮对话（保存 messages）
    config = {"configurable": {"thread_id": "weather_conversation"}}

    # 可以用user，content也可以直接传入Message类型
    # result = graph.invoke({"messages": [ ("user", "你好，我想查询深圳今天的天气") ]})
    result = graph.invoke({'messages': [HumanMessage(content="你好，我想查询深圳今天的天气")]})
    print(result)

    print("最终输出:", result['messages'][-1].content)