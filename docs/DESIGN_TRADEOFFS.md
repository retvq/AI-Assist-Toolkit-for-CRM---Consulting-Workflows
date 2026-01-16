# Design Tradeoffs

This document explains the key design decisions made in the AI Assist Toolkit and the rationale behind each choice.

## 1. Streamlit vs Full Frontend Framework

**Decision:** Use Streamlit instead of React/Vue/Next.js

**Pros:**
- Rapid development (hours vs days)
- Built-in session state management
- No frontend build complexity
- Python-native (consistent with AI/ML ecosystem)
- Live reload during development

**Cons:**
- Limited UI customization
- Not ideal for complex interactions
- Harder to unit test UI components

**Rationale:** For a demo-grade application, development speed matters more than pixel-perfect UI. Streamlit's simplicity allows focusing on the AI logic rather than frontend plumbing.

---

## 2. Groq API vs Other LLM Providers

**Decision:** Use Groq with Llama 3.3 70B

**Alternatives Considered:**
| Provider | Speed | Free Tier | Quality |
|----------|-------|-----------|---------|
| Groq | ⚡ Fastest | ✅ 30 RPM | High |
| OpenAI | Medium | ❌ Paid | Highest |
| Anthropic | Medium | ❌ Paid | Highest |
| Google Gemini | Fast | ✅ 15 RPM | High |
| Local Ollama | Slow | ✅ Free | Variable |

**Rationale:** Groq offers the best balance of speed, quality, and accessibility. Near-instant responses create better UX. Llama 3.3 70B is competitive with GPT-4 for structured tasks.

---

## 3. Deterministic-First Approach for Data Quality

**Decision:** Use Python/Pandas for data checks, AI only for explanation

**Why Not Full AI Analysis:**
- AI can hallucinate data issues that don't exist
- Deterministic checks are 100% reproducible
- Faster processing (no API calls for basic checks)
- Easier to debug and validate

**AI Role Limited To:**
- Explaining why issues matter (business context)
- Suggesting cleanup priorities
- Translating technical findings to stakeholder language

---

## 4. Fact vs Inference Separation

**Decision:** Explicitly label all AI inferences and separate from observed facts

**Implementation:**
- Observed facts use quotes from actual input
- Inferences prefixed with [Inferred] label
- Uncertainty section for unknowns

**Business Value:** Consultants using this tool with clients need to know which insights they can confidently share versus which require validation.

---

## 5. No Timelines/Assignments in Requirements Module

**Decision:** Explicitly exclude timelines, ownership, and architecture from AI output

**Rationale:**
- Timelines require team capacity knowledge
- Assignments require org chart knowledge
- Architecture requires technical constraints knowledge
- AI lacks this context → guesses would be harmful

**Trust Principle:** It's better to explicitly not provide something than to provide it incorrectly.

---

## 6. Session-Only Data (No Persistence)

**Decision:** No database, no file storage, no user accounts

**Pros:**
- Zero privacy/security risk for demo
- Simpler architecture
- Aligns with "all data is sensitive" assumption

**Cons:**
- Users can't save/resume work
- No analytics on usage patterns

**Production Path:** Add encrypted session storage + user auth when moving to production.

---

## 7. Single-Page vs Multi-Page App

**Decision:** Single page with tabs vs separate routes

**Rationale:**
- All three modules are equally important
- Users may switch between modules frequently
- Reduces cognitive load (no navigation needed)
- Faster module switching (no page loads)

---

## 8. Draft Watermarking

**Decision:** All AI outputs marked with "Draft – Requires Human Review"

**Implementation:**
- Prominent header on every output
- Footer reminder
- Cannot be removed programmatically

**Trust Principle:** Outputs should never be mistaken for final deliverables. The system is assistive, not authoritative.

---

## Summary: Core Design Philosophy

> "Would a consulting firm trust this as an internal assistant in front of a client?"

Every decision was filtered through this question:

| Principle | Implementation |
|-----------|----------------|
| Reliability over features | Deterministic checks first |
| Transparency over polish | Explicit fact/inference labeling |
| Safety over convenience | No autonomous actions |
| Trust over speed | Human review required for all outputs |
