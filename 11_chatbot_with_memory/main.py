from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

memory = MemorySaver()
# Compare this snippet with the previous one:

class ChatbotState(TypedDict):
    """
    State for the chatbot.
    """
    messages: Annotated[list, add_messages]

llm = ChatGroq(model="llama-3.3-70b-versatile")

def chat_node(state: ChatbotState) -> ChatbotState:
    """
    Node that handles the chat interaction.
    """
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    return state

graph = StateGraph(ChatbotState)

graph.add_node("chat", chat_node)

graph.set_entry_point("chat")
graph.set_finish_point("chat")

app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = app.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
    )
    print(response["messages"][-1].content)
