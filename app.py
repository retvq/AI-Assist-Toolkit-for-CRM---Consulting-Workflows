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
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Teal Theme with Glassmorphism
st.markdown("""
<style>
    /* Light theme background */
    .stApp {
        background-color: #f4f6f8 !important;
    }
    
    /* Animated logo */
    .logo-symbol {
        font-size: 4rem;
        color: #00838f;
        display: inline-block;
        animation: spin-decelerate 3s cubic-bezier(0.1, 0.9, 0.15, 1) forwards;
    }
    
    @keyframes spin-decelerate {
        0% { transform: rotate(0deg); opacity: 0; }
        20% { opacity: 1; }
        100% { transform: rotate(540deg); opacity: 1; }
    }
    
    /* Main header styling */
    .main-header {
        color: #1a1a1a !important;
        text-align: center;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
        padding: 2rem 0;
        border-bottom: 1px solid rgba(0, 131, 143, 0.15);
    }
    
    .main-header h1 {
        color: #00838f !important;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        animation: fade-in 1s ease-out forwards;
        animation-delay: 0.5s;
        opacity: 0;
    }
    
    @keyframes fade-in {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
        animation: fade-in 1s ease-out forwards;
        animation-delay: 0.8s;
        opacity: 0;
    }
    
    .tagline {
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
        animation: fade-in 1s ease-out forwards;
        animation-delay: 1.1s;
        opacity: 0;
    }
    
    /* Tab styling - teal theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0, 131, 143, 0.03);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 500;
        color: #1a1a1a !important;
        background: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 131, 143, 0.08) !important;
        color: #00838f !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(0, 131, 143, 0.15) !important;
        color: #00838f !important;
    }
    
    /* Tab button text - ensure dark by default */
    .stTabs [data-baseweb="tab"] button,
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {
        color: inherit !important;
    }
    
    /* Card styling with glassmorphism */
    .context-card {
        background: rgba(0, 131, 143, 0.03);
        border: 1px solid rgba(0, 131, 143, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    
    /* Answer/output box */
    .answer-box {
        background: rgba(0, 131, 143, 0.05);
        border: 1px solid rgba(0, 131, 143, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 0 20px rgba(0, 131, 143, 0.1);
    }
    
    /* Draft header styling */
    .draft-header {
        background: linear-gradient(135deg, #00838f 0%, #006064 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* All headings - ensure visibility in light theme */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #1a1a1a !important;
    }
    
    h1 {
        color: #00838f !important;
        font-weight: 700;
    }
    
    h2 {
        color: #00838f !important;
        font-weight: 600;
    }
    
    h3 {
        color: #00838f !important;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    h4 {
        color: #1a1a1a !important;
        font-weight: 500;
        border-bottom: 2px solid rgba(0, 131, 143, 0.2);
        padding-bottom: 0.5rem;
    }
    
    h5, h6 {
        color: #1a1a1a !important;
        font-weight: 500;
    }
    
    /* Primary button - teal theme */
    .stButton > button[kind="primary"],
    button[kind="primary"],
    .stFormSubmitButton > button {
        background-color: #00838f !important;
        border-color: #00838f !important;
        color: white !important;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button[kind="primary"]:hover,
    button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover {
        background-color: #006064 !important;
        border-color: #006064 !important;
        color: white !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 131, 143, 0.3);
    }
    
    /* Secondary button - dark text by default */
    .stButton > button:not([kind="primary"]) {
        background-color: transparent !important;
        border: 1px solid rgba(0, 131, 143, 0.4) !important;
        color: #1a1a1a !important;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stButton > button:not([kind="primary"]):hover {
        background-color: rgba(0, 131, 143, 0.1) !important;
        border-color: #00838f !important;
        color: #00838f !important;
    }
    
    /* Ensure all button text is visible */
    .stButton > button p,
    .stButton > button span {
        color: inherit !important;
    }
    
    /* ================================================
       LIGHT THEME - Form Elements Override
       Force light backgrounds, dark text for all inputs
       ================================================ */
    
    /* Text area - light background, dark text */
    .stTextArea textarea,
    .stTextArea [data-baseweb="textarea"],
    [data-testid="stTextArea"] textarea {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid rgba(0, 131, 143, 0.25) !important;
        border-radius: 8px !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #888 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00838f !important;
        box-shadow: 0 0 0 1px #00838f !important;
        background-color: #ffffff !important;
    }
    
    /* Text area label */
    .stTextArea label,
    .stTextArea label p {
        color: #1a1a1a !important;
    }
    
    /* Text input - light background */
    .stTextInput input,
    [data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 1px solid rgba(0, 131, 143, 0.25) !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input::placeholder {
        color: #888 !important;
    }
    
    .stTextInput label,
    .stTextInput label p {
        color: #1a1a1a !important;
    }
    
    /* Select box / dropdown */
    .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border-color: rgba(0, 131, 143, 0.25) !important;
    }
    
    .stSelectbox label,
    .stSelectbox label p {
        color: #1a1a1a !important;
    }
    
    /* File uploader - light theme */
    [data-testid="stFileUploader"],
    [data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: 1px dashed rgba(0, 131, 143, 0.3) !important;
        border-radius: 8px;
    }
    
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span {
        color: #1a1a1a !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #666 !important;
    }
    
    /* File uploader button */
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploaderDropzone"] button {
        background-color: rgba(0, 131, 143, 0.1) !important;
        color: #00838f !important;
        border: 1px solid rgba(0, 131, 143, 0.3) !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stFileUploader"] button:hover,
    [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: rgba(0, 131, 143, 0.2) !important;
        border-color: #00838f !important;
    }
    
    /* Expander styling - light theme */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary {
        background: rgba(0, 131, 143, 0.05) !important;
        border-radius: 8px;
        color: #1a1a1a !important;
    }
    
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid rgba(0, 131, 143, 0.1) !important;
        border-radius: 8px;
    }
    
    /* Data frame / table */
    .stDataFrame,
    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
    }
    
    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] td {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    /* Info/success/error boxes - ensure readable */
    .stAlert {
        border-radius: 8px;
    }
    
    .stAlert p {
        color: inherit !important;
    }
    
    /* All labels and markdown text */
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown span {
        color: #1a1a1a !important;
    }
    
    /* Override any dark-mode remnants */
    [data-baseweb="input"],
    [data-baseweb="textarea"],
    [data-baseweb="base-input"] {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #666;
        font-size: 0.85rem;
        border-top: 1px solid rgba(0, 131, 143, 0.15);
        margin-top: 3rem;
        background: rgba(0, 131, 143, 0.02);
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #00838f !important;
    }
    
    .stSpinner,
    .stSpinner > div,
    [data-testid="stSpinner"],
    [data-testid="stSpinner"] > div {
        color: #1a1a1a !important;
    }
    
    /* Spinner text */
    .stSpinner > div > span,
    [data-testid="stSpinner"] span {
        color: #1a1a1a !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: rgba(0, 131, 143, 0.1) !important;
        border-color: rgba(0, 131, 143, 0.3) !important;
        color: #00838f !important;
        border-radius: 8px;
    }
    
    .stDownloadButton > button:hover {
        background: rgba(0, 131, 143, 0.2) !important;
        border-color: #00838f !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid rgba(0, 131, 143, 0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdown"] li {
        color: #1a1a1a !important;
    }
    
    /* Radio buttons as nav items */
    [data-testid="stSidebar"] .stRadio > div {
        background: transparent;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(0, 131, 143, 0.03) !important;
        border: 1px solid rgba(0, 131, 143, 0.15) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin: 4px 0 !important;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label div {
        color: #1a1a1a !important;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(0, 131, 143, 0.08) !important;
        border-color: rgba(0, 131, 143, 0.3) !important;
    }
    
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] span,
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] p,
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] div {
        color: #00838f !important;
    }
    
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: rgba(0, 131, 143, 0.12) !important;
        border-color: #00838f !important;
    }
    
    /* Streamlit header toolbar - light theme */
    [data-testid="stHeader"],
    header[data-testid="stHeader"] {
        background-color: #f4f6f8 !important;
        border-bottom: 1px solid rgba(0, 131, 143, 0.1);
    }
    
    /* Toolbar buttons */
    [data-testid="stHeader"] button,
    [data-testid="stToolbar"] button {
        color: #00838f !important;
    }
    
    [data-testid="stToolbar"] {
        background-color: transparent !important;
    }
    
    /* Deploy button and menu */
    [data-testid="stStatusWidget"],
    [data-testid="stStatusWidget"] button {
        color: #00838f !important;
        background-color: transparent !important;
    }
    
    /* Hamburger menu icon / sidebar toggle - ALWAYS VISIBLE */
    /* Force the collapsed control to always show */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    div[data-testid="stSidebarCollapsedControl"],
    section[data-testid="stSidebarCollapsedControl"] {
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
        position: fixed !important;
        top: 0.75rem !important;
        left: 0.75rem !important;
        z-index: 999999 !important;
        pointer-events: auto !important;
        transform: none !important;
        transition: none !important;
    }
    
    /* Style the button inside */
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"] button,
    button[kind="header"],
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebarNavCollapseButton"] {
        color: #1a365d !important;
        background-color: #e2e8f0 !important;
        border: 2px solid #94a3b8 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
        opacity: 1 !important;
        visibility: visible !important;
        min-width: 40px !important;
        min-height: 40px !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button:hover,
    [data-testid="stSidebarCollapseButton"] button:hover {
        background-color: #cbd5e0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    /* Sidebar collapse button (X button) inside sidebar */
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebar"] button[aria-label="Close sidebar"] {
        color: #1a365d !important;
        background-color: #e2e8f0 !important;
        border: 2px solid #94a3b8 !important;
    }
    
    /* All header area buttons */
    header button,
    header button svg {
        color: #1a365d !important;
        fill: #1a365d !important;
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render the main application header."""
    st.markdown("""
    <div class="main-header">
        <div class="logo-symbol">&#10059;</div>
        <h1>AI Assist Toolkit</h1>
        <p class="sub-header">CRM & Consulting Workflows</p>
        <p class="tagline">Supporting Consultants, Not Replacing Them</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Collapsible info section
    with st.expander("About This Tool", expanded=False):
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
    st.markdown("### Lead / Opportunity Intelligence")
    st.markdown("_Reduce time spent understanding messy lead information_")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Input")
        
        # Sample data button
        if st.button("Load Sample Data", key="lead_sample"):
            st.session_state.lead_input = get_sample_lead_data()
            st.rerun()
        
        # Input text area
        lead_input = st.text_area(
            "Paste lead notes, email threads, or call summaries:",
            value=st.session_state.get("lead_input", ""),
            height=400,
            placeholder="Paste your lead information here...\n\nThis can include:\n- Email threads\n- Call notes or transcripts\n- CRM notes\n- Meeting summaries"
        )
        
        # Update session state
        st.session_state.lead_input = lead_input
        
        # Action buttons
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            process_btn = st.button("Analyze Lead", key="process_lead", type="primary", use_container_width=True)
        with button_col2:
            if st.button("Clear", key="clear_lead", use_container_width=True):
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
                    "Download as Markdown",
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
    st.markdown("### Requirement to Delivery Translation")
    st.markdown("_Convert client discussions into execution-ready drafts_")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Input")
        
        # Sample data button
        if st.button("Load Sample Data", key="req_sample"):
            st.session_state.req_input = get_sample_requirements_data()
            st.rerun()
        
        # Input text area
        req_input = st.text_area(
            "Paste discovery notes, requirements, or client messages:",
            value=st.session_state.get("req_input", ""),
            height=400,
            placeholder="Paste client requirements here...\n\nThis can include:\n- Discovery call notes\n- Client emails\n- Informal requirement descriptions\n- Meeting transcripts"
        )
        
        st.session_state.req_input = req_input
        
        # Action buttons
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            process_btn = st.button("Generate Documentation", key="process_req", type="primary", use_container_width=True)
        with button_col2:
            if st.button("Clear", key="clear_req", use_container_width=True):
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
                    "Download as Markdown",
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
    st.markdown("### CRM Data Quality & Readiness Check")
    st.markdown("_Identify data issues that could break automation or analytics_")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Input")
        
        # Sample data button
        if st.button("Load Sample Data", key="dq_sample"):
            sample_csv = get_sample_crm_data()
            st.session_state.dq_df = pd.read_csv(StringIO(sample_csv))
            st.session_state.dq_filename = "sample_crm_data.csv"
            st.rerun()
        
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
            process_btn = st.button("Analyze Data Quality", key="process_dq", type="primary", use_container_width=True)
        with button_col2:
            if st.button("Clear", key="clear_dq", use_container_width=True):
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
                    "Download Report",
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
        <p>All data is session-only and not stored. AI outputs require human review.</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with branding and navigation."""
    with st.sidebar:
        # Animated logo and branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 1.5rem 0; border-bottom: 1px solid rgba(0, 131, 143, 0.15);">
            <div class="logo-symbol" style="font-size: 3rem;">&#10059;</div>
            <h2 style="color: #00838f; margin: 0.5rem 0 0.2rem 0; font-size: 1.4rem;">AI Assist Toolkit</h2>
            <p style="color: #666; font-size: 0.85rem; margin: 0;">CRM & Consulting Workflows</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")  # Spacer
        
        # Module navigation
        st.markdown("### Select Module")
        
        module = st.radio(
            "Choose a workflow:",
            options=["Lead Intelligence", "Requirement Translation", "Data Quality Check"],
            index=["Lead Intelligence", "Requirement Translation", "Data Quality Check"].index(
                st.session_state.get("current_module", "Lead Intelligence")
            ),
            label_visibility="collapsed"
        )
        st.session_state.current_module = module
        
        st.divider()
        
        # About section
        with st.expander("About", expanded=False):
            st.markdown("""
            **Purpose:** Help consultants with CRM workflows
            
            **Modules:**
            - Lead Intelligence
            - Requirement Translation  
            - Data Quality Check
            
            **Note:** All outputs are drafts requiring human review.
            """)
        
        st.divider()
        
        # Footer info
        st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.75rem; padding-top: 1rem;">
            <p style="margin: 0;">Session-only data</p>
            <p style="margin: 0;">No data stored</p>
        </div>
        """, unsafe_allow_html=True)
    
    return module


def main():
    """Main application entry point."""
    # Initialize session state
    if "lead_input" not in st.session_state:
        st.session_state.lead_input = ""
    if "req_input" not in st.session_state:
        st.session_state.req_input = ""
    if "dq_df" not in st.session_state:
        st.session_state.dq_df = None
    if "current_module" not in st.session_state:
        st.session_state.current_module = "Lead Intelligence"
    
    # Render sidebar and get selected module
    selected_module = render_sidebar()
    
    # Render selected module in main area
    if selected_module == "Lead Intelligence":
        render_lead_intelligence_tab()
    elif selected_module == "Requirement Translation":
        render_requirement_translation_tab()
    elif selected_module == "Data Quality Check":
        render_data_quality_tab()
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()

