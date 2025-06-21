from typing import TypedDict

from langgraph.graph import StateGraph

class AgentState(TypedDict):
    """State for the personalized compliment agent."""
    name: str
    compliment: str = ""

def personalized_compliment_node(state: AgentState) -> AgentState:
    """A node that generates a personalized compliment."""
    state["compliment"] = f"{state['name']}, you have a wonderful smile!"
    return state

graph = StateGraph(AgentState)

graph.add_node("personalized_compliment", personalized_compliment_node)

graph.set_entry_point("personalized_compliment")
graph.set_finish_point("personalized_compliment")

app = graph.compile()

# with open("graph.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

result = app.invoke(AgentState(name="Alice"))

print(result)