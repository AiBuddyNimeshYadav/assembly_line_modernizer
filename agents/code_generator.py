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
        return f"Modernize the following code to current best practices."


def code_generator_node(state: AgentState):
    iteration = state.get("iteration_count", 0) + 1
    print(f"🔨 [CodeGenerator] Generating Code with Gemini (Attempt #{iteration})...")

    # 1. FETCH KEY INSIDE THE FUNCTION (Lazy Loading)
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("    ❌ ERROR: GOOGLE_API_KEY is missing. Check .env file.")
        return {"status": "failed", "compilation_errors": ["Missing API Key"]}

    # 2. Initialize Model on demand
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )
    except Exception as e:
        return {"status": "failed", "compilation_errors": [f"Model Init Error: {e}"]}

    if not state.get("is_ready_to_process"):
        return {"status": "blocked"}

    # 3. SELECT PROMPT BASED ON FILE TYPE
    file_type = state.get("file_type", "unknown")
    
    # Map file types to prompt files
    prompt_map = {
        "backend": "backend_java21_spring.txt",
        "jsf_view": "frontend_jsf_to_react.txt",
        "frontend_js": "frontend_jsf_to_react.txt",  # Reuse React prompt
        "build_ant": "build_ant_to_gradle.txt",
        "build_maven": "worker_prompt.txt",  # Use generic for Maven modernization
        "security_config": "security_config.txt",
        "config": "worker_prompt.txt",
        "unknown": "worker_prompt.txt"
    }
    
    prompt_file = prompt_map.get(file_type, "worker_prompt.txt")
    system_text = load_prompt(prompt_file)
    
    print(f"    Using prompt: {prompt_file} for type: {file_type}")

    # 4. Add Component Context for JSF Views
    user_content = f"Legacy Code:\n{state['legacy_content']}"
    
    if file_type == "jsf_view" and state.get("detected_components"):
        components = state["detected_components"]
        user_content += f"\n\nDetected PrimeFaces Components to Convert: {', '.join(components)}"
    
    # 5. Add Error Feedback Context (if any)
    if state.get("compilation_errors"):
        user_content += f"\n\nCRITICAL: The previous attempt failed with these errors. Fix them:\n{state['compilation_errors']}"

    # 6. Call Gemini
    messages = [
        SystemMessage(content=system_text),
        HumanMessage(content=user_content)
    ]

    try:
        response = llm.invoke(messages)
        code = response.content

        # Strip markdown fences if Gemini includes them
        # Handle multiple markdown languages
        for lang in ["java", "typescript", "tsx", "javascript", "gradle", "groovy", "kotlin", "xml"]:
            code = code.replace(f"```{lang}", "").replace("```", "")
        code = code.strip()

    except Exception as e:
        print(f"    Gemini Error: {e}")
        code = ""

    return {
        "modern_code": code,
        "iteration_count": iteration
    }