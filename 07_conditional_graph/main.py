"""
### ✅ Learning Objectives
* How to create a conditional graph with multiple nodes.
* How to route the flow of execution based on the state of the agent.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    """
    Represents the state of an agent.
    """
    number1: int
    operation: str
    number2: int
    finalNumber: int

def adder_node(state: AgentState) -> AgentState:
    """This function adds two numbers."""
    state["finalNumber"] = state["number1"] + state["number2"]
    return state

def subtractor_node(state: AgentState) -> AgentState:
    """This function subtracts two numbers."""
    state["finalNumber"] = state["number1"] - state["number2"]
    return state

def operation_router(state: AgentState) -> Literal["addition_operation", "subtraction_operation"]:
    """This function routes to the appropriate operation based on the operation type."""
    if state["operation"] == "+":
        return "addition_operation"
    elif state["operation"] == "-":
        return "subtraction_operation"
    else:
        raise ValueError(f"Unknown operation: {state['operation']}")
    
graph = StateGraph(AgentState)

graph.add_node("addition_node", adder_node)
graph.add_node("subtraction_node", subtractor_node)

graph.add_conditional_edges(
    START,
    operation_router,
    {
        "addition_operation": "addition_node",
        "subtraction_operation": "subtraction_node"
    }
)
graph.add_edge("addition_node", END)
graph.add_edge("subtraction_node", END)

app = graph.compile()

# with open("graph.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

result = app.invoke(AgentState(number1=10, operation="+", number2=5))
print(f"Result of addition: {result['finalNumber']}")

result = app.invoke(AgentState(number1=10, operation="-", number2=5))
print(f"Result of subtraction: {result['finalNumber']}")