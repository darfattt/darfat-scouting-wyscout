"""
Test script to verify Ollama setup before running the chatbot
Run this to diagnose connection issues: python chatbot/test_ollama_connection.py
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_ollama_package():
    """Test if ollama package is installed"""
    print("\n" + "="*60)
    print("TEST 1: Ollama Package Installation")
    print("="*60)
    try:
        import ollama
        import importlib.metadata
        print(importlib.metadata.version("ollama"))
        print(f"✅ ollama package imported successfully")
        print(f"   Package version: {ollama.__version__ if hasattr(ollama, '__version__') else 'unknown'}")
        return True
    except ImportError as e:
        print(f"❌ ollama package not found: {e}")
        print("\nFix: pip install ollama>=0.3.0")
        return False

def test_server_connection():
    """Test connection to Ollama server"""
    print("\n" + "="*60)
    print("TEST 2: Ollama Server Connection")
    print("="*60)
    try:
        import ollama
        print("Using:", ollama.__file__)
        models = ollama.list()
        print(f"✅ Connected to Ollama server at http://localhost:11434")
        print(f"   Available models: {len(models.get('models', []))}")
        return True, models
    except Exception as e:
        print(f"❌ Failed to connect to Ollama server")
        print(f"   Error: {str(e)}")
        print("\nFix:")
        print("1. Open a new terminal")
        print("2. Run: ollama serve")
        print("3. Keep that terminal open")
        print("4. Run this test again")
        return False, None

def get_model_id(m: dict) -> str | None:
    return m.get("name") or m.get("model")

def test_required_models(models_response):
    """Test if required models are downloaded"""
    print("\n" + "="*60)
    print("TEST 3: Required Models")
    print("="*60)

    required_models = {
        "phi3:mini": "Chat generation model",
        "nomic-embed-text:latest": "Embedding model"
    }

    if not models_response:
        print("❌ Cannot check models (server not connected)")
        return False

    available_models = {
        get_model_id(m): m
        for m in models_response.get("models", [])
        if get_model_id(m)
    }

    all_present = True
    for model_name, description in required_models.items():
        # Check exact match or partial match (some versions might differ)
        exact_match = model_name in available_models
        partial_match = any(model_name.split(':')[0] in name for name in available_models.keys())

        if exact_match or partial_match:
            matched_name = model_name if exact_match else next(
                name for name in available_models.keys()
                if model_name.split(':')[0] in name
            )
            size = available_models[matched_name].get('size', 'unknown')
            # Convert size to GB if it's a number
            if isinstance(size, (int, float)):
                size_gb = size / (1024**3)
                size_str = f"{size_gb:.2f} GB"
            else:
                size_str = str(size)
            print(f"✅ {model_name}: {description}")
            print(f"   (Found: {matched_name}, Size: {size_str})")
        else:
            print(f"❌ {model_name}: {description} - NOT FOUND")
            print(f"   Fix: ollama pull {model_name}")
            all_present = False

    return all_present

def test_ollama_client():
    """Test MyOllamaClient initialization"""
    print("\n" + "="*60)
    print("TEST 4: MyOllamaClient Initialization")
    print("="*60)
    try:
        from chatbot.ollama_client.my_ollama_client import MyOllamaClient
        client = MyOllamaClient()
        print("✅ MyOllamaClient initialized successfully")
        print(f"   Chat model: {client.chat_model}")
        print(f"   Embed model: {client.embed_model}")
        print(f"   Host: {client.host}")
        return True, client
    except Exception as e:
        print(f"❌ Failed to initialize MyOllamaClient")
        print(f"   Error: {str(e)}")
        return False, None

def test_chat_generation(client):
    """Test chat generation"""
    print("\n" + "="*60)
    print("TEST 5: Chat Generation")
    print("="*60)
    if not client:
        print("❌ Cannot test chat (client not initialized)")
        return False

    try:
        messages = [{"role": "user", "content": "Say hello in one word"}]
        response = client.generate_chat(messages)
        print(f"✅ Chat generation working")
        print(f"   Test response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Chat generation failed")
        print(f"   Error: {str(e)}")
        return False

def test_embedding_generation(client):
    """Test embedding generation"""
    print("\n" + "="*60)
    print("TEST 6: Embedding Generation")
    print("="*60)
    if not client:
        print("❌ Cannot test embeddings (client not initialized)")
        return False

    try:
        embedding = client.generate_embedding("test text")
        print(f"✅ Embedding generation working")
        print(f"   Embedding dimensions: {len(embedding)}")
        print(f"   Sample values: {embedding[:5]}...")
        return True
    except Exception as e:
        print(f"❌ Embedding generation failed")
        print(f"   Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🔍 OLLAMA SETUP VERIFICATION")
    print("=" * 60)
    print("This script tests your Ollama setup for the chatbot")
    print("=" * 60)

    results = []

    # Test 1: Package installation
    package_ok = test_ollama_package()
    results.append(("Package Installation", package_ok))

    if not package_ok:
        print_summary(results)
        return

    # Test 2: Server connection
    server_ok, models_response = test_server_connection()
    results.append(("Server Connection", server_ok))

    if not server_ok:
        print_summary(results)
        return

    # Test 3: Required models
    models_ok = test_required_models(models_response)
    results.append(("Required Models", models_ok))

    # Test 4: MyOllamaClient
    client_ok, client = test_ollama_client()
    results.append(("MyOllamaClient Init", client_ok))

    if not client_ok:
        print_summary(results)
        return

    # Test 5: Chat generation
    chat_ok = test_chat_generation(client)
    results.append(("Chat Generation", chat_ok))

    # Test 6: Embedding generation
    embed_ok = test_embedding_generation(client)
    results.append(("Embedding Generation", embed_ok))

    # Print summary
    print_summary(results)

def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(passed for _, passed in results)

    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\nYou're ready to run the chatbot:")
        print("  conda activate python_310_env")
        print("  streamlit run chatbot/chatbot_app.py")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the issues above before running the chatbot.")
        print("See chatbot/README.md for detailed setup instructions.")
    print()

if __name__ == "__main__":
    main()
