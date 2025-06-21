"""
### ✅ Learning Objectives
* How to create a graph with a loop.
* How to use a loop condition to control the flow of execution.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    """
    Represents the state of an agent.
    """
    name: str
    greeting: str
    numbers: list[int]
    counter: int

def greeting_node(state: AgentState) -> AgentState:
    """This function greets the agent."""
    state["greeting"] = f"Hello, {state['name']}!"
    state["counter"] = 0
    return state

def random_number_node(state: AgentState) -> AgentState:
    """This function generates a random number and adds it to the list."""
    import random
    number = random.randint(1, 100)
    state["numbers"].append(number)
    state["counter"] += 1
    return state

def loop_condition(state: AgentState) -> bool:
    """This function checks if the counter is less than 5."""
    return state["counter"] < 5

graph = StateGraph(AgentState)

graph.add_node("greeting_node", greeting_node)
graph.add_node("random_number_node", random_number_node)

graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node", "random_number_node")
graph.add_conditional_edges(
    "random_number_node",
    loop_condition,
    {
        True: "random_number_node",
        False: END
    }
)

app = graph.compile()

# with open("graph.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

result = app.invoke(AgentState(name="Bob", numbers=[]))
print("Final State:", result)