from app.graph.workflow import app as graph_app

def test_graph_compiles():
    # Simple test to ensure the graph compiles
    assert graph_app is not None
