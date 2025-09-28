import streamlit as st

st.set_page_config(page_title="Prompt Enhancer", page_icon="📝")
st.title("📝 Prompt Engineer — ICDC Prompt Enhancer")
st.caption("Demo Mode - Learn how to structure better prompts with ICDC!")

# Input Section
st.subheader("Enter ICDC Elements")
instruction = st.text_area("Instruction", value="Rewrite my draft for clarity and brevity")
context = st.text_area("Context", value="Audience: busy professionals; Goal: concise and actionable", height=100)
demonstration = st.text_area("Demonstration (Example)", value="Input: 'Write long email' → Output: 'Draft concise 3-sentence email'", height=100)
constraint = st.text_area("Constraint", value="Max 3 bullets, ≤12 words each", height=80)

st.divider()

st.subheader("Paste your rough prompt")
draft = st.text_area("Your draft prompt:", height=140, placeholder="Type or paste your draft prompt here...")

# Button
if st.button("✨ Enhance Prompt"):
    if not draft.strip():
        st.warning("Please enter a draft prompt.")
    else:
        # Demo output with ICDC
        framework_output = (
            f"*INSTRUCTION*: {instruction}\n\n"
            f"*CONTEXT*: {context}\n\n"
            f"*DEMONSTRATION*:\n{demonstration}\n\n"
            f"*CONSTRAINT*: {constraint}\n\n"
            f"*USER DRAFT:*\n{draft}"
        )

        st.success("Enhanced Prompt (Demo Mode)")
        st.markdown("### 📝 Structured Prompt (ICDC)")
        st.markdown(framework_output)

        st.download_button("📥 Copy Enhanced Prompt", framework_output, file_name="enhanced_prompt.txt")