import streamlit as st
st.set_page_config(page_title="Prompt Enhancers", page_icon="🔧")
st.title("🔧 Prompt Engineer – General Prompt Enhancer")
st.caption("Demo Mode - Learn how to structure better prompts!")

st.subheader("Enter CC-SC-R Framework")

# Context
context = st.text_area(
    "1. Context", 
    value="Audience: busy professional; Goal: clear and specific communication",
    help="What's the background? Who is the audience? What's the goal?"
)

# Constraint
constraint = st.text_area(
    "2. Constraint", 
    value="Keep response under 200 words; Use simple language; No jargon",
    help="What are the limitations or requirements? (length, style, format, etc.)"
)

# Structure
structure = st.text_input(
    "3. Structure", 
    value="3 bullet points with headers",
    help="How should the output be organized?"
)

# Checkpoint
checkpoint = st.text_input(
    "4. Checkpoint", 
    value="Verify clarity and completeness before finalizing",
    help="What validation step should happen mid-process?"
)

# Review
review = st.text_input(
    "5. Review", 
    value="Ask 1 clarifying question at the end",
    help="What follow-up or review step is needed?"
)

st.subheader("Paste your rough prompt")
draft = st.text_area("Your draft prompt:", height=140)

if st.button("Enhance Prompt"):

    if not draft.strip():
        st.warning("Please enter a draft prompt.")
    else:
        # Demo output - shows CC-SC-R structured approach
        instruction = (
            "Generate an enhanced, structured prompt using CC-SC-R Framework.\n"
            "Apply all 5 components to improve the prompt.\n"
        )
        demo_output = (
            f"CONTEXT: {context}\n\n"
            f"CONSTRAINT: {constraint}\n\n"
            f"STRUCTURE: {structure}\n\n"
            f"CHECKPOINT: {checkpoint}\n\n"
            f"REVIEW: {review}\n\n"
            f"USER DRAFT:\n{draft}\n\n"
            "---\n"
            "ENHANCED PROMPT PREVIEW:\n"
            f"Given the context above, rewrite the following with these constraints: {constraint}\n"
            f"Format as: {structure}\n"
            f"Validate: {checkpoint}\n"
            f"Finally: {review}"
        )
        
        st.success("Enhanced Prompt (Demo Mode)")
        st.code(instruction + "\n" + demo_output, language="markdown")
        
        st.info("💡 This is demo mode showing the CC-SC-R structure. In live mode, AI would generate the actual enhanced prompt!")