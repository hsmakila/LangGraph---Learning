"""
### ✅ Learning Objectives
* How to create a simple chatbot using LangGraph and LangChain Groq.
* How to make llm calls within a LangGraph node.
"""

from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

class ChatbotState(TypedDict):
    """
    State for the chatbot.
    """
    messages: list[HumanMessage]

llm = ChatGroq(model="llama-3.3-70b-versatile")

def chat_node(state: ChatbotState) -> ChatbotState:
    """
    Node that handles the chat interaction.
    """
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    return state

graph = StateGraph(ChatbotState)

graph.add_node("chat", chat_node)

graph.set_entry_point("chat")
graph.set_finish_point("chat")

app = graph.compile()

result = app.invoke(
    ChatbotState(messages=[HumanMessage(content="Hello, how are you?")])
)
print(result["messages"][-1].content)

while True:
    user_input = input("\n\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    result = app.invoke(
        ChatbotState(messages=[HumanMessage(content=user_input)])
    )
    print("Bot:", result["messages"][-1].content)