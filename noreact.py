from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from llm_utils import llm
from langchain_core.messages import HumanMessage
from draw import save_graph_as_png

# 1. 手动创建工具节点
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
tool_node = ToolNode(tools)

# 2. 手动绑定工具到模型
model_with_tools = llm.bind_tools(tools)

# 3. 手动定义条件路由函数 路由函数需要返回特定的规则目标 之后在太你家条件边的时候进行指定
def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 4. 手动定义智能体节点
def call_model(state: MessagesState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

# 5. 手动构建状态图
workflow = StateGraph(MessagesState)

# 6. 手动添加节点
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# 7. 手动定义边和条件边
workflow.add_edge(START, "agent")
workflow.add_edge("tools", "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})

# 8. 手动编译图
app = workflow.compile()


result = app.invoke({'messages': [HumanMessage(content="你好，我想查询深圳今天的天气")]})
print(result)

print("最终输出:", result['messages'][-1].content)

save_graph_as_png(app, "./graphs/c3/noreact.png")