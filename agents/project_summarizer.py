import os
from typing import List, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

def load_prompt(filename):
    path = os.path.join("prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

import time
import random

def generate_project_summary(project_context: Dict, specs: List[str], output_dir: str):
    """
    Aggregates individual file specifications into a single project-level summary.
    """
    print(f"\n📑 [ProjectSummarizer] Generating consolidated project report...")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("    ⚠️  Skipping summary: GOOGLE_API_KEY missing")
        return

    # Prepare content
    specs_content = ""
    for spec_path in specs:
        try:
            with open(spec_path, "r", encoding="utf-8") as f:
                content = f.read()
                name = os.path.basename(spec_path).replace(".spec.md", "")
                preview = content[:1000] + "..." if len(content) > 1000 else content
                specs_content += f"\n--- Component: {name} ---\n{preview}\n"
        except Exception as e:
            print(f"    ⚠️  Could not read spec {spec_path}: {e}")

    template = load_prompt("project_summary.txt")
    
    context_str = f"""
Tech Stack: {', '.join(project_context.get('tech_stack', []))}
Dependencies: {', '.join(project_context.get('dependencies', []))}
Packages: {', '.join(project_context.get('packages', []))}
"""

    prompt = template.format(
        project_context=context_str,
        specs=specs_content
    )

    # Retry Logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0,
                google_api_key=api_key
            )
            
            response = llm.invoke([HumanMessage(content=prompt)])
            summary = response.content
            
            # Save Report
            report_path = os.path.join(output_dir, "project_summary.md")
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(summary)
                
            print(f"    ✅ Project Summary saved: {report_path}")
            return report_path

        except Exception as e:
            if "429" in str(e):
                wait_time = (2 ** attempt) * 10 + random.randint(1, 5)
                print(f"    ⚠️  Rate limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"    ❌ Error generating project summary: {e}")
                return None
    
    print("    ❌ Failed to generate summary after retries.")
    return None
