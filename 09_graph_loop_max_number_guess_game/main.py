"""
### ✅ Learning Objectives
* How to use a loop condition to control the flow of execution.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import random

class AgentState(TypedDict):
    """
    Represents the state of an agent.
    """
    number: int
    guesses: list[int]
    attempts: int
    hint: str

def setup_node(state: AgentState) -> AgentState:
    """Initialize the game with a random number and reset attempts."""
    state["guesses"] = [0]
    state["attempts"] = 0
    state["hint"] = "higher"
    return state

def guess_node(state: AgentState) -> AgentState:
    """Guess the number based on the hint."""
    if state["hint"] == "higher":
        state["guesses"].append(random.randint(state["guesses"][-1] + 1, 20))
    else:
        state["guesses"].append(random.randint(1, state["guesses"][-1] - 1))
    state["attempts"] += 1
    
    return state

def hint_node(state: AgentState) -> AgentState:
    """Provide a hint based on the last guess."""
    if state["guesses"][-1] < state["number"]:
        state["hint"] = "higher"
    elif state["guesses"][-1] > state["number"]:
        state["hint"] = "lower"
    else:
        state["hint"] = "correct"
    
    return state

def loop_condition(state: AgentState) -> bool:
    """Check if the last guess is correct or if attempts are less than 5."""
    return state["hint"] != "correct" and state["attempts"] < 7

graph = StateGraph(AgentState)

graph.add_node("setup_node", setup_node)
graph.add_node("guess_node", guess_node)
graph.add_node("hint_node", hint_node)

graph.add_edge(START, "setup_node")
graph.add_edge("setup_node", "guess_node")
graph.add_edge("guess_node", "hint_node")
graph.add_conditional_edges(
    "hint_node",
    loop_condition,
    {
        True: "guess_node",
        False: END
    }
)
app = graph.compile()

# with open("graph.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

for event in app.stream(AgentState(number=10)):
    print(event)