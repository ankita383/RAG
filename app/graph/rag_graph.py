from langgraph.graph import StateGraph

def build_graph(rag_node):
    workflow = StateGraph(dict)
    workflow.add_node("rag", rag_node)
    workflow.set_entry_point("rag")
    graph = workflow.compile()
    return graph