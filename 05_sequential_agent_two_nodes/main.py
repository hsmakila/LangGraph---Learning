"""
### ✅ Learning Objectives
* How to define and connect **multiple nodes** in a graph to create a sequence of operations.
* How to pass and update state progressively through multiple nodes.
* How to build a composite message by combining outputs from different nodes.
* Reinforce managing state mutations in a multi-step workflow.
"""

from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    """
    Represents the state of an agent.
    """
    name: str
    age: int
    final: str

def first_node(state: AgentState) -> AgentState:
    """This function sets the final to greet the user."""
    state["final"] = f"Hello {state['name']}!"
    return state

def second_node(state: AgentState) -> AgentState:
    """This function appends the age to the final message."""
    state["final"] = f"{state['final']} You are {state['age']} years old."
    return state

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.set_finish_point("second_node")

app = graph.compile()

# with open("graph.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

result = app.invoke(AgentState(name="Alice", age=30))
print(result)
