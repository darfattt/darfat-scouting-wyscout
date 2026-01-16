"""
Test script to verify chatbot imports work
"""
import sys
from pathlib import Path

# Add project root to path (script is in chatbot/, need to go up one more level)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print(f"Project root: {project_root}")
print(f"Python path: {sys.path[:3]}")

try:
    print("\n=== Testing Imports ===")
    
    print("1. Testing chatbot.ollama.client...")
    from chatbot.ollama_client.my_ollama_client import MyOllamaClient
    print("   ✓ MyOllamaClient imported")
    
    print("2. Testing chatbot.vector_store.chroma_wrapper...")
    from chatbot.vector_store.chroma_wrapper import ChromaWrapper
    print("   ✓ ChromaWrapper imported")
    
    print("3. Testing chatbot.retrieval.query_processor...")
    from chatbot.retrieval.query_processor import QueryProcessor
    print("   ✓ QueryProcessor imported")
    
    print("4. Testing chatbot.retrieval.context_builder...")
    from chatbot.retrieval.context_builder import ContextBuilder
    print("   ✓ ContextBuilder imported")
    
    print("5. Testing chatbot.response.generator...")
    from chatbot.response.generator import ResponseGenerator
    print("   ✓ ResponseGenerator imported")
    
    print("6. Testing chatbot.utils.viz_utils...")
    from chatbot.utils.viz_utils import create_radar_chart, create_comparison_bar, create_scatter_plot
    print("   ✓ Visualization functions imported")
    
    print("\n7. Testing utils.data_loader...")
    import utils.data_loader as data_loader
    print("   ✓ data_loader imported")
    print(f"   Available functions: {dir(data_loader)[:10]}")
    
    print("\n=== All imports successful! ===")
    
except Exception as e:
    print(f"\n❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
