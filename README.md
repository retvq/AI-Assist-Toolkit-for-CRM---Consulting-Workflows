# AI Assist Toolkit for CRM & Consulting Workflows

A demo-grade, production-aligned AI assistant that supports consultants across three CRM-centric workflows.


![AIAssistToolkitforCRMConsultingWorkflows-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/848cec12-14b8-42e8-bdfe-272608163958)

Live at [StreamLit](https://ai-assist-toolkit-for-crm.streamlit.app/)

## 🎯 Features

### Module 1: Lead/Opportunity Intelligence
- Analyzes messy lead notes, email threads, and call summaries
- Separates **observed facts** from **AI inferences**
- Generates CRM-ready summaries with suggested next actions

### Module 2: Requirement to Delivery Translation
- Converts client discussions into structured user stories
- Creates acceptance criteria and task breakdowns
- **Never** estimates timelines or assigns ownership

### Module 3: CRM Data Quality Check
- Detects missing fields, duplicates, and format issues
- Uses deterministic checks (no AI guessing)
- AI explains business impact with cleanup priorities

## 🚀 Quick Start

### 1. Clone and Setup
```bash
cd "AI Assist Toolkit for CRM & Consulting Workflows"
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Groq API key
# Get a free key at: https://console.groq.com/keys
```

### 3. Run the Application
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## 📁 Project Structure

```
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
│
├── core/
│   ├── llm_client.py          # Groq API wrapper
│   ├── validators.py          # Input validation utilities
│   └── formatters.py          # Output formatting utilities
│
├── modules/
│   ├── lead_intelligence.py   # Module 1
│   ├── requirement_translator.py  # Module 2
│   └── data_quality.py        # Module 3
│
├── sample_data/
│   ├── sample_leads.txt       # Demo lead notes
│   ├── sample_requirements.txt # Demo requirements
│   └── sample_crm_data.csv    # Demo CRM data with issues
│
└── docs/
    ├── SYSTEM_FLOW.md         # System flow documentation
    ├── DESIGN_TRADEOFFS.md    # Design decisions
    └── PRODUCTION_NOTES.md    # Production considerations
```

## 🔑 Design Principles

1. **Human-in-the-loop** - All outputs are drafts requiring human review
2. **Deterministic first** - Data quality checks use code, not AI guessing
3. **Explicit uncertainty** - AI clearly labels facts vs inferences
4. **Session-only data** - Nothing is stored beyond your current session
5. **No autonomous actions** - The system assists, never decides

## 📊 Sample Data

The `sample_data/` folder contains realistic test data:

- **sample_leads.txt** - Email thread and call notes for a B2B SaaS lead
- **sample_requirements.txt** - Discovery call notes for a logistics startup
- **sample_crm_data.csv** - CRM export with intentional quality issues:
  - Missing contact names
  - Duplicate records
  - Invalid email formats
  - Negative deal amounts
  - Inconsistent phone formats

## 🔧 Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Framework | Streamlit | Rapid prototyping, built-in session state |
| LLM | Groq (Llama 3.3 70B) | Fast inference, generous free tier |
| Data | Pandas | Standard for CSV/tabular processing |

## 📝 License

Demo project - for evaluation purposes.


