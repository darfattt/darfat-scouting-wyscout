"""
Football Scout Chatbot - Main Streamlit Interface
AI-powered football player analysis assistant using local LLM (Ollama)
"""
import streamlit as st
import os
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import chatbot components
from chatbot.ollama_client.my_ollama_client import MyOllamaClient
from chatbot.vector_store.chroma_wrapper import ChromaWrapper
from chatbot.retrieval.query_processor import QueryProcessor
from chatbot.retrieval.context_builder import ContextBuilder
from chatbot.response.generator import ResponseGenerator
from chatbot.utils.chat_memory import ChatMemory

# Import existing utils and config
import utils.data_loader as data_loader
from config.stat_categories import STAT_CATEGORIES
from config.composite_attributes import COMPOSITE_ATTRIBUTES

# Page configuration
st.set_page_config(
    page_title="Football Scout Assistant",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
TEST_CSVS = ['BRI Liga 1 25-26.csv', 'Brazil Serie B 2025.csv']
ALL_CSVS = None  # Will load all CSVs for production
MAX_CHAT_HISTORY = 5


def init_session_state():
    """Initialize all session state variables"""
    if 'my_ollama_client' not in st.session_state:
        try:
            st.session_state.my_ollama_client = MyOllamaClient()
            st.session_state.db_initialized = False
        except ConnectionError as e:
            st.error("### ❌ Ollama Server Not Running")
            st.error(str(e))
            st.info(
                "**Quick Start:**\n\n"
                "1. Open a new terminal and run: `ollama serve`\n"
                "2. Keep that terminal open\n"
                "3. Refresh this page\n\n"
                "See `chatbot/README.md` for detailed setup instructions."
            )
            st.stop()
        except Exception as e:
            st.error(f"❌ Unexpected error initializing Ollama client: {str(e)}")
            st.stop()
    
    if 'chroma_wrapper' not in st.session_state:
        st.session_state.chroma_wrapper = ChromaWrapper()
        st.session_state.chroma_wrapper.set_ollama_client(st.session_state.my_ollama_client)
    
    if 'chat_memory' not in st.session_state:
        st.session_state.chat_memory = ChatMemory(MAX_CHAT_HISTORY)
    
    if 'query_processor' not in st.session_state:
        st.session_state.query_processor = QueryProcessor(st.session_state.my_ollama_client)
    
    if 'context_builder' not in st.session_state:
        st.session_state.context_builder = ContextBuilder(st.session_state.chroma_wrapper)
    
    if 'response_generator' not in st.session_state:
        st.session_state.response_generator = ResponseGenerator(st.session_state.my_ollama_client)
    
    if 'use_test_csvs' not in st.session_state:
        st.session_state.use_test_csvs = True  # Default to test mode
    
    if 'db_initialized' not in st.session_state:
        st.session_state.db_initialized = False
    
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""


def initialize_database():
    """Initialize vector database with player data"""
    if st.session_state.db_initialized:
        player_count = st.session_state.chroma_wrapper.get_collection_count("players")
        st.success(f"✓ Vector DB loaded with {player_count} players")
        return
    
    with st.spinner("Initializing vector database..."):
        data_folder = os.path.join(os.getcwd(), "data", "2025")
        
        if not os.path.exists(data_folder):
            st.error(f"Data folder not found: {data_folder}")
            st.stop()
        
        # Load and prepare data
        df_players = data_loader.load_all_league_data(data_folder)
        
        # Get stat columns
        stat_columns = data_loader.get_all_stat_columns(STAT_CATEGORIES)
        
        # Calculate percentiles
        df_players = data_loader.calculate_percentiles(df_players, stat_columns)
        
        # Calculate composite attributes
        df_composite = data_loader.calculate_composite_attributes_batch(
            df_players,
            stat_columns,
            COMPOSITE_ATTRIBUTES
        )
        
        # Index players
        csvs_to_index = TEST_CSVS if st.session_state.use_test_csvs else ALL_CSVS
        
        player_count = st.session_state.chroma_wrapper.index_players(
            df_players,
            df_composite,
            csvs_to_index
        )
        
        # Index knowledge
        all_presets = {}
        for preset_file in ['defender_presets', 'forward_presets', 
                           'attacking_midfielder_presets', 'fullback_presets',
                           'midfielder_presets']:
            try:
                preset_module = __import__(f"config.{preset_file}", fromlist=[preset_file])
                all_presets.update(getattr(preset_module, 
                                           f"{preset_file.replace('_', '').upper()}_PRESETS", {}))
            except:
                pass
        
        knowledge_count = st.session_state.chroma_wrapper.index_knowledge(
            COMPOSITE_ATTRIBUTES,
            all_presets
        )
        
        st.session_state.db_initialized = True
        st.success(f"✓ Indexed {player_count} players and {knowledge_count} knowledge items")


def render_sidebar():
    """Render sidebar with database status and chat controls"""
    with st.sidebar:
        st.header("Recruitment Analysis Assistant")
        
        # Database status
        st.subheader("Database Status")
        if st.session_state.db_initialized:
            player_count = st.session_state.chroma_wrapper.get_collection_count("players")
            st.success(f"✓ {player_count} players indexed")
        else:
            st.warning("⚠️ Database not initialized")
        
        # Data source selection (development mode only)
        st.divider()
        st.subheader("Data Source")
        use_test = st.radio(
            "CSV Files to Index:",
            options=["Test (2 files, ~750 players)", "All (200+ files, ~10K+ players)"],
            horizontal=True,
            help="Test mode: Faster indexing for development\nProduction mode: All players from data/2025/"
        )
        st.session_state.use_test_csvs = (use_test == "Test (2 files, ~750 players)")
        
        # Chat controls
        st.divider()
        st.subheader("Chat Controls")
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_memory.clear()
            st.rerun()
        
        if st.button("🔄 Rebuild Database"):
            st.session_state.chroma_wrapper.clear_collection("players")
            st.session_state.chroma_wrapper.clear_collection("knowledge")
            st.session_state.db_initialized = False
            st.rerun()
        
        # Quick suggestions
        st.divider()
        st.subheader("Quick Queries")
        suggestions = [
            "Find CBs under 25 with Security > 80",
            "Compare top scorers from BRI Liga 1",
            "Who fits ball-playing CB role best in Brazil Serie B?",
            "Show stats for top scorer in BRI Liga 1",
            "Find midfielders with Creativity > 85"
        ]
        
        for suggestion in suggestions:
            if st.button(suggestion, key=f"suggestion_{suggestion[:20]}"):
                st.session_state.input_text = suggestion


def render_chat_interface():
    """Render main chat interface"""
    st.title("⚽ Football Recruitment Analysis Assistant")
    
    # Initialize session state
    init_session_state()
    
    # Initialize database if needed
    if not st.session_state.db_initialized:
        initialize_database()
    
    # Chat messages container
    chat_container = st.container()
    
    # Display existing messages
    with chat_container:
        for msg in st.session_state.chat_memory.get_history():
            if msg['role'] == 'user':
                st.chat_message("user").write(msg['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(msg['content'])
    
    # Chat input
    user_input = st.chat_input(
        "Ask about players, roles, or stats...",
        key="chat_input"
    )
    
    if user_input:
        # Process query
        with st.spinner("Analyzing..."):
            query_result = st.session_state.query_processor.process_query(user_input)
            
            # Build context
            context = st.session_state.context_builder.build_context(query_result)
            
            # Generate response
            response = st.session_state.response_generator.generate_response(
                user_input,
                context,
                st.session_state.chat_memory.get_history()
            )
        
        # Add to memory
        st.session_state.chat_memory.add_message('user', user_input)
        st.session_state.chat_memory.add_message('assistant', response['text'])
        
        # Display new messages
        with chat_container:
            st.chat_message("user").write(user_input)
            
            with st.chat_message("assistant"):
                st.write(response['text'])
                
                # Display visualizations
                if response['visualizations']:
                    for chart in response['visualizations']:
                        st.plotly_chart(chart, use_container_width=True)
        
        # Clear input
        st.rerun()


def main():
    """Main execution function"""
    init_session_state()
    render_sidebar()
    render_chat_interface()


if __name__ == "__main__":
    main()
