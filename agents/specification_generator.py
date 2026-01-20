import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from core.state import AgentState

def load_prompt(filename: str) -> str:
    """Load prompt template from prompts directory"""
    prompt_path = os.path.join("prompts", filename)
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Generate a detailed technical specification for the following code."

def specification_generator_node(state: AgentState):
    print(f"📄 [SpecGenerator] Analyzing file for specification...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("    ❌ ERROR: GOOGLE_API_KEY is missing.")
        return {"status": "failed"}

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )
    except Exception as e:
        print(f"    ❌ Model Init Error: {e}")
        return {"status": "failed"}

    # Prepare Prompt
    template = load_prompt("specification_generation.txt")
    content = state.get("legacy_content", "")
    filename = os.path.basename(state.get("legacy_filepath", "unknown"))
    file_type = state.get("file_type", "unknown")
    
    # Get Project Context (if available)
    project_context = state.get("project_context", {})
    context_str = ""
    if project_context:
        context_str = f"""
Project Context:
- Tech Stack: {', '.join(project_context.get('tech_stack', []))}
- Packages: {', '.join(project_context.get('packages', [])[:10])}... (total {len(project_context.get('packages', []))})
- Dependencies: {', '.join(project_context.get('dependencies', [])[:10])}...
"""

    # Fill template
    prompt_text = template.format(
        filename=filename,
        file_type=file_type,
        content_length=len(content),
        content=content
    )
    
    if context_str:
        prompt_text = context_str + "\n" + prompt_text

    messages = [HumanMessage(content=prompt_text)]

    try:
        response = llm.invoke(messages)
        spec = response.content.strip()
        print(f"    ✅ Specification generated ({len(spec)} chars)")
        return {"specification": spec}
    except Exception as e:
        print(f"    ❌ Generation Error: {e}")
        return {"status": "failed"}
