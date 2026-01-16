"""
AI Assist Toolkit for CRM & Consulting Workflows
Main Streamlit Application

A demo-grade, production-aligned AI assistant for consultants.
"""
import streamlit as st
import pandas as pd
from io import StringIO

from modules.lead_intelligence import process_lead_intelligence, get_sample_lead_data
from modules.requirement_translator import process_requirement_translation, get_sample_requirements_data
from modules.data_quality import process_data_quality_check, get_sample_crm_data


# Page configuration
st.set_page_config(
    page_title="AI Assist Toolkit - CRM & Consulting",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main container styling */
    .main > div {
        padding-top: 1rem;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 1rem 0 2rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
    }
    
    /* Output container styling */
    .output-container {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    /* Success message styling */
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Warning styling */
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Draft header styling */
    .draft-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #666;
        font-size: 0.85rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render the main application header."""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Assist Toolkit</h1>
        <h3>CRM & Consulting Workflows</h3>
        <p><em>Supporting Consultants, Not Replacing Them</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Collapsible info section
    with st.expander("ℹ️ About This Tool", expanded=False):
        st.markdown("""
        This AI assistant helps consultants with three key workflows:
        
        1. **Lead Intelligence** - Quickly understand messy lead information
        2. **Requirement Translation** - Convert client discussions into execution-ready drafts  
        3. **Data Quality Check** - Detect CRM data issues before they cause problems
        
        **Important:**
        - All outputs are drafts requiring human review
        - No data is stored beyond your current session
        - AI insights are clearly labeled as inferences
        """)


def render_lead_intelligence_tab():
    """Render the Lead Intelligence module tab."""
    st.markdown("### 📋 Lead / Opportunity Intelligence")
    st.markdown("_Reduce time spent understanding messy lead information_")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Input")
        
        # Sample data button
        if st.button("📝 Load Sample Data", key="lead_sample"):
            st.session_state.lead_input = get_sample_lead_data()
        
        # Input text area
        lead_input = st.text_area(
            "Paste lead notes, email threads, or call summaries:",
            value=st.session_state.get("lead_input", ""),
            height=400,
            key="lead_text_area",
            placeholder="Paste your lead information here...\n\nThis can include:\n- Email threads\n- Call notes or transcripts\n- CRM notes\n- Meeting summaries"
        )
        
        # Update session state
        st.session_state.lead_input = lead_input
        
        # Action buttons
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            process_btn = st.button("🔍 Analyze Lead", key="process_lead", type="primary", use_container_width=True)
        with button_col2:
            if st.button("🗑️ Clear", key="clear_lead", use_container_width=True):
                st.session_state.lead_input = ""
                st.session_state.lead_output = None
                st.rerun()
    
    with col2:
        st.markdown("#### Output")
        
        if process_btn and lead_input:
            with st.spinner("Analyzing lead information..."):
                result = process_lead_intelligence(lead_input)
                st.session_state.lead_output = result
        
        # Display output
        if st.session_state.get("lead_output"):
            result = st.session_state.lead_output
            if result["success"]:
                st.markdown(result["output"])
                # Copy button
                st.download_button(
                    "📋 Download as Markdown",
                    result["output"],
                    file_name="lead_analysis.md",
                    mime="text/markdown"
                )
            else:
                st.error(result["error"])
        else:
            st.info("Enter lead information and click 'Analyze Lead' to generate insights.")


def render_requirement_translation_tab():
    """Render the Requirement Translation module tab."""
    st.markdown("### 📝 Requirement to Delivery Translation")
    st.markdown("_Convert client discussions into execution-ready drafts_")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Input")
        
        # Sample data button
        if st.button("📝 Load Sample Data", key="req_sample"):
            st.session_state.req_input = get_sample_requirements_data()
        
        # Input text area
        req_input = st.text_area(
            "Paste discovery notes, requirements, or client messages:",
            value=st.session_state.get("req_input", ""),
            height=400,
            key="req_text_area",
            placeholder="Paste client requirements here...\n\nThis can include:\n- Discovery call notes\n- Client emails\n- Informal requirement descriptions\n- Meeting transcripts"
        )
        
        st.session_state.req_input = req_input
        
        # Action buttons
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            process_btn = st.button("📋 Generate Documentation", key="process_req", type="primary", use_container_width=True)
        with button_col2:
            if st.button("🗑️ Clear", key="clear_req", use_container_width=True):
                st.session_state.req_input = ""
                st.session_state.req_output = None
                st.rerun()
    
    with col2:
        st.markdown("#### Output")
        
        if process_btn and req_input:
            with st.spinner("Generating documentation..."):
                result = process_requirement_translation(req_input)
                st.session_state.req_output = result
        
        if st.session_state.get("req_output"):
            result = st.session_state.req_output
            if result["success"]:
                st.markdown(result["output"])
                st.download_button(
                    "📋 Download as Markdown",
                    result["output"],
                    file_name="requirements_draft.md",
                    mime="text/markdown"
                )
            else:
                st.error(result["error"])
        else:
            st.info("Enter requirements and click 'Generate Documentation' to create user stories and task breakdowns.")


def render_data_quality_tab():
    """Render the Data Quality Check module tab."""
    st.markdown("### 📊 CRM Data Quality & Readiness Check")
    st.markdown("_Identify data issues that could break automation or analytics_")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Input")
        
        # Sample data button
        if st.button("📝 Load Sample Data", key="dq_sample"):
            sample_csv = get_sample_crm_data()
            st.session_state.dq_df = pd.read_csv(StringIO(sample_csv))
            st.session_state.dq_filename = "sample_crm_data.csv"
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload CRM data (CSV):",
            type=["csv"],
            key="dq_uploader"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.dq_df = df
                st.session_state.dq_filename = uploaded_file.name
            except Exception as e:
                st.error(f"Error reading file: {e}")
        
        # Show data preview if available
        if st.session_state.get("dq_df") is not None:
            st.markdown(f"**File:** {st.session_state.get('dq_filename', 'Unknown')}")
            st.markdown(f"**Rows:** {len(st.session_state.dq_df)} | **Columns:** {len(st.session_state.dq_df.columns)}")
            
            with st.expander("Preview Data", expanded=False):
                st.dataframe(st.session_state.dq_df.head(10), use_container_width=True)
        
        # Action buttons
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            process_btn = st.button("🔍 Analyze Data Quality", key="process_dq", type="primary", use_container_width=True)
        with button_col2:
            if st.button("🗑️ Clear", key="clear_dq", use_container_width=True):
                st.session_state.dq_df = None
                st.session_state.dq_output = None
                st.session_state.dq_filename = None
                st.rerun()
    
    with col2:
        st.markdown("#### Output")
        
        if process_btn and st.session_state.get("dq_df") is not None:
            with st.spinner("Analyzing data quality..."):
                result = process_data_quality_check(st.session_state.dq_df)
                st.session_state.dq_output = result
        
        if st.session_state.get("dq_output"):
            result = st.session_state.dq_output
            if result["success"]:
                st.markdown(result["output"])
                st.download_button(
                    "📋 Download Report",
                    result["output"],
                    file_name="data_quality_report.md",
                    mime="text/markdown"
                )
            else:
                st.error(result["error"])
        else:
            st.info("Upload a CSV file and click 'Analyze Data Quality' to check for issues.")


def render_footer():
    """Render the application footer."""
    st.markdown("""
    <div class="footer">
        <p><strong>AI Assist Toolkit</strong> - Demo Application</p>
        <p>All data is session-only and not stored. AI outputs require human review.</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    # Initialize session state
    if "lead_input" not in st.session_state:
        st.session_state.lead_input = ""
    if "req_input" not in st.session_state:
        st.session_state.req_input = ""
    if "dq_df" not in st.session_state:
        st.session_state.dq_df = None
    
    # Render header
    render_header()
    
    # Create tabs for the three modules
    tab1, tab2, tab3 = st.tabs([
        "🎯 Lead Intelligence",
        "📝 Requirement Translation", 
        "📊 Data Quality Check"
    ])
    
    with tab1:
        render_lead_intelligence_tab()
    
    with tab2:
        render_requirement_translation_tab()
    
    with tab3:
        render_data_quality_tab()
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
