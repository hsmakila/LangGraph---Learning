from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph import START, END

class AgentState(TypedDict):
    message: str

def greeting_node(state: AgentState) -> AgentState:
    """A node that greets the user."""
    state["message"] = f"Hi {state['message']}! How is your day?"
    return state

graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", END)

app = graph.compile()

# with open("graph.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

result = app.invoke(AgentState(message="Bob"))

print(result)