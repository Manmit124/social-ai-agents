from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import plan_node, generate_node, validate_node, hashtag_node, finalize_node


def create_agent_graph():
    """
    Create the LangGraph state graph for tweet generation agent.
    
    Returns:
        Compiled state graph
    """
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("plan", plan_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("add_hashtags", hashtag_node)
    workflow.add_node("finalize", finalize_node)
    
    # Define the edges (flow)
    workflow.set_entry_point("plan")
    
    # Plan -> Generate
    workflow.add_edge("plan", "generate")
    
    # Generate -> Validate
    workflow.add_edge("generate", "validate")
    
    # Validate -> Hashtags (if valid) or END (if invalid)
    workflow.add_conditional_edges(
        "validate",
        lambda state: "add_hashtags" if state.get("is_valid") else "end",
        {
            "add_hashtags": "add_hashtags",
            "end": END
        }
    )
    
    # Hashtags -> Finalize
    workflow.add_edge("add_hashtags", "finalize")
    
    # Finalize -> END
    workflow.add_edge("finalize", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


async def run_agent(user_prompt: str, platform: str = "twitter") -> AgentState:
    """
    Run the tweet generation agent.
    
    Args:
        user_prompt: User's input prompt
        platform: Target platform (twitter, linkedin, reddit)
        
    Returns:
        Final agent state with generated tweet
    """
    # Create the agent graph
    app = create_agent_graph()
    
    # Initialize state
    initial_state: AgentState = {
        "user_prompt": user_prompt,
        "platform": platform,
        "tweet_content": "",
        "hashtags": [],
        "final_content": "",
        "char_count": 0,
        "is_valid": False,
        "error": None,
        "step": "start"
    }
    
    # Run the agent
    final_state = await app.ainvoke(initial_state)
    
    return final_state


