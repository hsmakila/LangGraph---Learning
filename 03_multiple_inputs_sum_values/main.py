"""
### ✅ Learning Objectives
* How to design a state that accepts **multiple inputs** (e.g. a list and a string).
* How to operate on multiple fields from the state within a single node.
"""

from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    """
    Represents the state of an agent.
    """
    values: list[int]
    name: str
    results: str

def sum_values(state: AgentState) -> AgentState:
    """This function sums the values in the state and returns a new state with the result."""
    state['results'] = f"Hi there, {state['name']}! You sum = {sum(state['values'])}."
    return state

graph = StateGraph(AgentState)

graph.add_node("sum_values", sum_values)

graph.set_entry_point("sum_values")
graph.set_finish_point("sum_values")

app = graph.compile()

result = app.invoke(AgentState(
    values=[1, 2, 3, 4, 5],
    name="John"
))

print(result)