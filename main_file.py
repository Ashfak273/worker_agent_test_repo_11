from langgraph.graph import StateGraph, END
from typing import TypedDict

# Define the shared state between agents
class AgentState(TypedDict):
    task: str
    plan: str
    research: str
    code: str

# Simulated agent logic — replace with LangChain LLM chains if needed
def planner_agent(state: AgentState) -> AgentState:
    print("🧠 Planner Agent running...")
    plan = "1. Research weather APIs\n2. Get API key\n3. Write function using requests"
    return {**state, "plan": plan}

def researcher_agent(state: AgentState) -> AgentState:
    print("🔍 Researcher Agent running...")
    research = "Best free API is OpenWeatherMap. Endpoint: api.openweathermap.org/data/2.5/weather"
    return {**state, "research": research}

def coder_agent(state: AgentState) -> AgentState:
    print("💻 Coder Agent running...")
    code = """import requests

def get_weather(city, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    return response.json()
"""
    return {**state, "code": code}

# Create the LangGraph state graph
graph = StateGraph(AgentState)

# Add agent nodes
graph.add_node("planner", planner_agent)
graph.add_node("researcher", researcher_agent)
graph.add_node("coder", coder_agent)

# Define edges (flow)
graph.set_entry_point("planner")
graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "coder")
graph.add_edge("coder", END)

# Compile the graph
app = graph.compile()

# Invoke the graph with initial state
if __name__ == "__main__":
    result = app.invoke({"task": "Build a Python function to get weather data"})
    
    print("\n--- PLAN ---\n", result["plan"])
    print("\n--- RESEARCH ---\n", result["research"])
    print("\n--- CODE ---\n", result["code"])
