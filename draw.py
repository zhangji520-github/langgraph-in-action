import os

def save_graph_as_png(graph, filename):
    """Saves the Mermaid diagram of the graph as a PNG file."""
    # 创建目录（如果不存在）
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    graph_bytes = graph.get_graph().draw_mermaid_png()
    with open(filename, "wb") as f:
        f.write(graph_bytes)
    