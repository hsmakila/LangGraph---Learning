"""
### ✅ Learning Objectives
* How to implement **conditional logic** in a node based on a state field.
* How to perform different operations (e.g., sum or product) based on user input.
* Continue reinforcing use of multi-field state and custom computation logic.
"""

from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    """
    Represents the state of an agent.
    """
    values: list[int]
    name: str
    operation: str
    results: str

def conditional_operation(state: AgentState) -> AgentState:
    """This function performs a conditional operation based on the 'operation' field in the state."""
    if state["operation"] == "+":
        operation_result = sum(state["values"])
    elif state["operation"] == "*":
        operation_result = 1
        for value in state["values"]:
            operation_result *= value
    else:
        raise ValueError(f"Unsupported operation: {state['operation']}")
    
    state["results"] = f"Hi there, {state['name']}! Your result = {operation_result}."
    return state

graph = StateGraph(AgentState)

graph.add_node("conditional_operation", conditional_operation)
graph.set_entry_point("conditional_operation")
graph.set_finish_point("conditional_operation")

app = graph.compile()

result = app.invoke(AgentState(
    values=[1, 2, 3, 4, 5],
    name="John",
    operation="+"
))

print(result)

result = app.invoke(AgentState(
    values=[1, 2, 3, 4, 5],
    name="John",
    operation="*"
))

print(result)

