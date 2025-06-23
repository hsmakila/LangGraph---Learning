import os
from textwrap import dedent

from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain_tavily import TavilySearch
from newsapi import NewsApiClient


class ReactAgentState(TypedDict):
    """
    State for the React agent.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def sum(a: int, b: int) -> int:
    """
    A simple tool that sums two integers.
    """
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """
    A simple tool that subtracts two integers.
    """
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """
    A simple tool that multiplies two integers.
    """
    return a * b

newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_API_KEY"))

@tool
def get_latest_news(query: str) -> str:
    """
    Fetches top news articles related to the query using NewsAPI.
    Returns a formatted string of titles and URLs.
    """
    articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy', page_size=5)
    if not articles['articles']:
        return "No news articles found for your query."
    
    results = []
    for article in articles['articles']:
        title = article['title']
        url = article['url']
        results.append(f"- {title}\n  {url}")
    
    return "\n".join(results)

google_search = TavilySearch(max_results=2, topic="general")

tools = [sum, subtract, multiply, google_search, get_latest_news]

llm = ChatGroq(model="qwen/qwen3-32b").bind_tools(tools, parallel_tool_calls=False)

def react_agent_node(state: ReactAgentState) -> ReactAgentState:
    """
    Node that handles the React agent interaction.
    """
    system_message = SystemMessage(
        content=dedent("""
            You are a expert in news headlines. You always follow below steps to generate a news headline and summary:
            1. Take a topic from the user.
            2. User get_latest_news tool to get latest news related to the topic.
            3. Pick one news article from the results.
            4. Fetch additional information about the news article using google_search tool.
            5. Generate a news headline and summary based on the information fetched.
        """)
    )
    response = llm.invoke([system_message] + state["messages"])
    return {"messages": [response]}

def should_continue(state: ReactAgentState) -> bool:
    """
    Continue if last message has tool call
    """
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return False
    return True

graph = StateGraph(ReactAgentState)

graph.add_node("react_agent", react_agent_node)
graph.add_node("tool_node", ToolNode(tools=tools))

graph.add_edge(START, "react_agent")
graph.add_conditional_edges(
    "react_agent",
    should_continue,
    {
        True: "tool_node",
        False: END
    }
)
graph.add_edge("tool_node", "react_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

input = {"messages": [
    # HumanMessage(content="Who are the current presidents of USA and Sri Lanka and what is the age gap between them?"),
    HumanMessage(content="Write a news headline and summary about the latest news on AI.")
]}
print_stream(app.stream(input, stream_mode="values"))

