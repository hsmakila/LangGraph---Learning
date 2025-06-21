"""
### ✅ Learning Objectives
* How to extend multi-node sequences to handle complex state updates over several steps.
* How to work with lists in state and convert them into formatted strings.
* How to progressively build and append information to a single state field across nodes.
* How to visualize the full graph with multiple nodes connected sequentially.
"""

from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    """
    Represents the state of an agent.
    """
    name: str
    age: int
    skills: list[str]
    result: str

def first_node(state: AgentState) -> AgentState:
    """This function only sets the greeting."""
    state["result"] = f"{state['name']}, welcome to the agent system!"
    return state

def second_node(state: AgentState) -> AgentState:
    """This function appends the age to the result message."""
    state["result"] += f" You are {state['age']} years old."
    return state

def third_node(state: AgentState) -> AgentState:
    """This function appends the skills to the result message."""
    skills_str = ", ".join(state["skills"])
    state["result"] += f" Your have skills in: {skills_str}."
    return state

graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.set_finish_point("third_node")

app = graph.compile()

# with open("graph.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

result = app.invoke(AgentState(name="Alice", age=30, skills=["Python", "AI", "Data Science"]))
print(result["result"])