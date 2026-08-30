from typing import TypedDict
import json
import os
from groq import Groq
from langgraph.graph import StateGraph, END
from tools.schemas import tools as schema_tools
from tools.get_deals import get_deals, update_deal_stage, schedule_meeting, send_email

class AgentState(TypedDict):
    query: str
    plan: list
    current_step: int
    tool_result: dict
    verified: bool
    retries: int

available_functions = {
    "get_deals": get_deals,
    "update_deal_stage": update_deal_stage,
    "schedule_meeting": schedule_meeting,
    "send_email": send_email,
}

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def planner_node(state: AgentState):
    query = state.get("query", "")
    messages = [
        {"role": "system", "content": "You are a sales agent."},
        {"role": "user", "content": query}
    ]
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=0.3,
        tools=schema_tools,
        tool_choice="auto"
    )
    
    msg = response.choices[0].message
    
    plan = []
    if getattr(msg, "tool_calls", None):
        for t in msg.tool_calls:
            plan.append({
                "function_name": t.function.name,
                "arguments": json.loads(t.function.arguments),
                "id": t.id
            })
            
    return {"plan": plan, "current_step": 0, "retries": 0, "verified": False}

def selector_node(state: AgentState):
    return state # Pass-through

def executor_node(state: AgentState):
    plan = state["plan"]
    current_step = state["current_step"]
    
    if current_step >= len(plan):
        return {"tool_result": {}}
        
    step = plan[current_step]
    func_name = step["function_name"]
    args = step["arguments"]
    
    func = available_functions[func_name]
    try:
        res = func(**args)
    except Exception as e:
        res = {"success": False, "error": str(e)}
        
    return {"tool_result": res}

def verifier_node(state: AgentState):
    plan = state["plan"]
    current_step = state["current_step"]
    if current_step >= len(plan):
        return {"verified": True}
        
    step = plan[current_step]
    func_name = step["function_name"]
    args = step["arguments"]
    tool_result = state.get("tool_result", {})
    
    verified = False
    
    if func_name == "update_deal_stage":
        company = args.get("company", "")
        expected_stage = args.get("new_stage", "")
        deal = get_deals(company)
        if deal.get("stage") == expected_stage:
            verified = True
    elif func_name == "schedule_meeting":
        company = args.get("company", "")
        expected_date = args.get("date", "")
        deal = get_deals(company)
        if deal.get("meeting_date") == expected_date:
            verified = True
    else:
        # Default verification for other tools
        if tool_result.get("success", False):
            verified = True
            
    return {"verified": verified}

def router_node(state: AgentState):
    if state["current_step"] >= len(state["plan"]):
        return "end"
        
    if state["verified"]:
        return "next_step"
    else:
        if state["retries"] < 3:
            return "retry"
        else:
            return "end"

def increment_step(state: AgentState):
    return {"current_step": state["current_step"] + 1, "retries": 0, "verified": False}

def increment_retry(state: AgentState):
    return {"retries": state["retries"] + 1}

# Graph setup
graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.add_node("selector", selector_node)
graph.add_node("executor", executor_node)
graph.add_node("verifier", verifier_node)
graph.add_node("increment_step", increment_step)
graph.add_node("increment_retry", increment_retry)

graph.set_entry_point("planner")
graph.add_edge("planner", "selector")
graph.add_edge("selector", "executor")
graph.add_edge("executor", "verifier")

graph.add_conditional_edges(
    "verifier",
    router_node,
    {
        "next_step": "increment_step",
        "retry": "increment_retry",
        "end": END
    }
)
graph.add_edge("increment_step", "selector")
graph.add_edge("increment_retry", "executor")

app = graph.compile()

def run_llm(content: str):
    initial_state = {
        "query": content,
        "plan": [],
        "current_step": 0,
        "tool_result": {},
        "verified": False,
        "retries": 0
    }
    
    final_state = app.invoke(initial_state)
    return final_state
