from dotenv import load_dotenv

load_dotenv(  )

from typing import Literal

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END, START, StateGraph, MessagesState

from chains import first_responder, revisor
from tool_executor import execute_tools

MAX_ITERATIONS = 2

def draft_node(state: MessagesState):
    """draft the initial response."""
    response = first_responder.invoke({"messages":state["messages"]})
    return {"messages": [response]}

def revise_node(state: MessagesState):
    """revise the answer based on tool results."""
    response = revisor.invoke({"messages":state["messages"]})
    return {"messages": [response]}

def event_loop(state: MessagesState) -> Literal["execute_tools", END]:
    """determine whether to continue or end based on iteration count. """
    count_tool_visits = sum(isinstance(m, ToolMessage) for m in state["messages"])

    if count_tool_visits < MAX_ITERATIONS:
        return "execute_tools"
    else:
        return END
    
builder = StateGraph(MessagesState)
builder.add_node("draft", draft_node)
builder.add_node("revise", revise_node)
builder.add_node("execute_tools", execute_tools)
builder.add_edge(START, "draft")
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")
builder.add_conditional_edges("revise", event_loop, ["execute_tools", END])

graph = builder.compile()

print(graph.get_graph().draw_mermaid())

res = graph.invoke(
    {
        "messages": [
            {
                "role":"user",
                "content":"write about AI powered SOC / autonomous SOC problem domain, list startups that do that and raised capital."
            }
        ]
    }
)

last_message = res["messages"][-1]
if isinstance(last_message, AIMessage) and last_message.tool_calls:
    print(last_message.tool_calls[0]["args"]["answer"])
print(res)