import os
import re
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from core.state import AgentState


def classify_with_ai(content: str, filepath: str) -> tuple[str, str]:
    """
    Uses AI to classify unknown file types based on content analysis.
    Returns: (file_type, target_extension)
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("    ⚠️  WARNING: Cannot use AI classification - GOOGLE_API_KEY missing")
        return "unknown", ".txt"
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )
        
        system_prompt = """You are a code file classifier for legacy application modernization.

Analyze the provided file content and classify it into ONE of these categories:
- backend: Java backend code (controllers, services, repositories)
- jsf_view: JSF/PrimeFaces XHTML views or JSP files
- frontend_js: Frontend JavaScript code
- build_ant: Ant build files
- build_maven: Maven POM files
- security_config: Security configuration files
- config: Other configuration files
- unknown: Cannot determine

For each classification, also suggest the target file extension for modernization:
- backend → .java (Spring Boot)
- jsf_view → .tsx (React TypeScript)
- frontend_js → .ts (TypeScript)
- build_ant → .gradle (Gradle)
- build_maven → .xml (modernized Maven)
- security_config → .java (SecurityConfig class)
- config → (keep original extension)
- unknown → .txt

Respond in this EXACT format (two lines only):
file_type: <type>
target_extension: <extension>

Example:
file_type: backend
target_extension: .java"""
        
        # Truncate content if too long (avoid token limits)
        content_preview = content[:2000] if len(content) > 2000 else content
        
        user_message = f"""File: {filepath}

Content:
{content_preview}"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        
        response = llm.invoke(messages)
        result = response.content.strip()
        
        # Parse response
        file_type = "unknown"
        target_ext = ".txt"
        
        for line in result.split('\n'):
            if line.startswith('file_type:'):
                file_type = line.split(':', 1)[1].strip()
            elif line.startswith('target_extension:'):
                target_ext = line.split(':', 1)[1].strip()
        
        print(f"    🤖 AI Classification: {file_type} → {target_ext}")
        return file_type, target_ext
        
    except Exception as e:
        print(f"    ⚠️  AI Classification failed: {e}")
        return "unknown", ".txt"


def classifier_node(state: AgentState):
    path = state['legacy_filepath']
    print(f"\n🔍 [Classifier] Classifying: {path}...")

    try:
        # Read file content
        if not state.get('legacy_content'):
            with open(path, 'r', encoding="utf-8") as f:
                content = f.read()
        else:
            content = state['legacy_content']
    except Exception as e:
        return {"status": "failed", "compilation_errors": [str(e)]}

    # Extract filename
    filename = os.path.basename(path).lower()
    
    # ENHANCED CLASSIFICATION LOGIC
    file_type = "unknown"
    target_ext = ".txt"
    detected_components = []
    frontend_framework = "react"  # Default
    ui_library = "primereact"  # Default

    # 1. JSF XHTML Views (Frontend)
    if path.endswith(".xhtml"):
        file_type = "jsf_view"
        target_ext = ".tsx"
        
        # Detect PrimeFaces components
        primefaces_pattern = r'<p:(\w+)'
        components = re.findall(primefaces_pattern, content)
        detected_components = [f"p:{comp}" for comp in set(components)]
        
        if detected_components:
            print(f"    Found PrimeFaces components: {', '.join(detected_components[:5])}")
    
    # 2. Legacy JSP Views
    elif path.endswith(".jsp"):
        file_type = "jsf_view"
        target_ext = ".tsx"
    
    # 3. Frontend JavaScript (Legacy)
    elif path.endswith(".js") and "src" in path.lower():
        file_type = "frontend_js"
        target_ext = ".ts"  # Convert to TypeScript
    
    # 4. Ant Build Files
    elif filename == "build.xml":
        file_type = "build_ant"
        target_ext = ".gradle"  # or .gradle.kts for Kotlin DSL
    
    # 5. Maven Build Files
    elif filename == "pom.xml":
        file_type = "build_maven"
        target_ext = ".xml"  # Keep as XML but modernize content
    
    # 6. Security Configuration
    elif filename == "web.xml":
        file_type = "security_config"
        target_ext = ".java"  # Will become SecurityConfig.java
    
    # 7. Java Backend
    elif path.endswith(".java"):
        # Check if it's a JSF managed bean or regular backend
        if "@ManagedBean" in content or "javax.faces" in content:
            file_type = "backend"  # Will be converted to Spring
            print(f"    Detected JSF Managed Bean → Will convert to Spring")
        else:
            file_type = "backend"
        target_ext = ".java"
    
    # 8. Other Config Files
    elif path.endswith((".xml", ".properties", ".yml", ".yaml")):
        file_type = "config"
        target_ext = os.path.splitext(path)[1]
    
    # 9. AI Fallback for Unknown Types
    else:
        print(f"    ⚠️  Unknown file type - using AI classification...")
        file_type, target_ext = classify_with_ai(content, path)
    
    print(f"    Type: {file_type.upper()} | Target: {target_ext}")

    return {
        "legacy_content": content,
        "file_type": file_type,
        "target_extension": target_ext,
        "detected_components": detected_components if detected_components else None,
        "frontend_framework": frontend_framework if file_type in ["jsf_view", "frontend_js"] else None,
        "ui_library": ui_library if file_type == "jsf_view" else None,
        "iteration_count": 0,
        "status": "in_progress"
    }