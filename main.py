import os
import json
import time
import argparse
import sys
import shutil
import shutil
import zipfile
import yaml
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

# --- 1. Load Environment Variables ---
dotenv_path = find_dotenv()
if not dotenv_path:
    print("⚠️  WARNING: .env file not found. Please create it.")
else:
    load_dotenv(dotenv_path)

# Import Logic
from langgraph.graph import StateGraph, END
from agents.classifier import classifier_node
from agents.dependency_check import dependency_check_node
from agents.architect import architect_node
from agents.code_generator import code_generator_node
from agents.validator import validator_node
from agents.specification_generator import specification_generator_node
from core.state import AgentState
from core.project_scanner import ProjectScanner
from agents.project_summarizer import generate_project_summary

# --- 2. Configuration ---
DEFAULT_CONFIG_PATH = "config.yaml"

def load_config(config_path):
    """Loads configuration from a YAML file."""
    if not os.path.exists(config_path):
        # Fallback to defaults if config file is missing
        print(f"⚠️  Config file '{config_path}' not found. Using defaults.")
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"❌ Error loading config file: {e}")
        return {}

# Default Constants (Fallback)
DEFAULT_INPUT_DIR = "workspace/input_legacy"
DEFAULT_OUTPUT_DIR = "workspace/output_modern"
DEFAULT_SPECS_DIR = "workspace/output_specs"
TEMP_DIR = "workspace/temp_extracted"


def router(state: AgentState):
    """Determines the next step based on Validator feedback"""
    status = state.get("status")

    if status == "retry":
        if state["iteration_count"] >= 3:
            return "failed"
        return "retry"

    if status == "complete":
        return "complete"

    return "failed"


def build_workflow():
    """
    Compiles the Agent Graph with all 5 agents:
    Classifier → DependencyCheck → Architect → CodeGenerator → Validator
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("classifier", classifier_node)
    workflow.add_node("dependency_check", dependency_check_node)
    workflow.add_node("architect", architect_node)
    workflow.add_node("code_generator", code_generator_node)
    workflow.add_node("validator", validator_node)

    workflow.set_entry_point("classifier")

    workflow.add_edge("classifier", "dependency_check")
    workflow.add_edge("dependency_check", "architect")
    workflow.add_edge("architect", "code_generator")
    workflow.add_edge("code_generator", "validator")

    workflow.add_conditional_edges(
        "validator",
        router,
        {
            "retry": "code_generator",  # Retry goes back to code_generator
            "complete": END,
            "failed": END
        }
    )

    return workflow.compile()


def process_file(app, filepath, root_dir, output_dir, reports_dir, project_context=None):
    """Runs the workflow for a single file and saves output with JSON report."""
    # Calculate relative path to mirror structure (e.g. services/UserService.java)
    rel_path = os.path.relpath(filepath, root_dir)
    print(f"\n🔄 Processing: {rel_path}...")

    initial_state = {
        "legacy_filepath": filepath, 
        "status": "pending",
        "project_context": project_context or {} # Pass context
    }
    start_time = datetime.now()

    try:
        result = app.invoke(initial_state)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Prepare JSON report data
        report = {
            "metadata": {
                "original_file": rel_path,
                "original_path": filepath,
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": round(duration, 2),
                "status": result.get("status", "unknown")
            },
            "classification": {
                "file_type": result.get("file_type", "unknown"),
                "target_extension": result.get("target_extension", "unknown"),
                "detected_components": result.get("detected_components", []),
                "frontend_framework": result.get("frontend_framework"),
                "ui_library": result.get("ui_library")
            },
            "transformation": {
                "modernization_plan": result.get("modernization_plan", "No plan generated"),
                "iteration_count": result.get("iteration_count", 0),
                "compilation_errors": result.get("compilation_errors")
            }
        }

        if result["status"] == "complete":
            # Use target extension from transformation
            target_ext = result.get("target_extension", os.path.splitext(filepath)[1])
            
            # Change file extension based on transformation
            base_name = os.path.splitext(rel_path)[0]
            new_rel_path = base_name + target_ext
            
            # Construct Output Paths
            output_path = os.path.join(output_dir, new_rel_path)
            report_path = os.path.join(reports_dir, base_name + ".report.json")
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            os.makedirs(os.path.dirname(report_path), exist_ok=True)

            # Save modernized code
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result["modern_code"])
            
            # Add output info to report
            report["output"] = {
                "code_file": new_rel_path,
                "code_file_absolute": output_path,
                "report_file": base_name + ".report.json",
                "lines_of_code": len(result["modern_code"].splitlines())
            }
            
            # Save JSON report
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            print(f"    ✅ Success! Saved to: {output_path}")
            print(f"    📊 Report saved to: {report_path}")
            return True, None
        else:
            errors = result.get("compilation_errors", ["Unknown Error"])
            report["error"] = {
                "errors": errors,
                "failed_at_iteration": result.get("iteration_count", 0)
            }
            
            # Save error report
            base_name = os.path.splitext(rel_path)[0]
            report_path = os.path.join(reports_dir, base_name + ".report.json")
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"    ❌ Failed. Errors: {errors}")
            print(f"    📊 Error report saved to: {report_path}")
            return False, errors

    except Exception as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Save exception report
        error_report = {
            "metadata": {
                "original_file": rel_path,
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": round(duration, 2),
                "status": "exception"
            },
            "error": {
                "type": "runtime_exception",
                "message": str(e),
                "exception_class": type(e).__name__
            }
        }
        
        base_name = os.path.splitext(rel_path)[0]
        report_path = os.path.join(reports_dir, base_name + ".report.json")
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(error_report, f, indent=2, ensure_ascii=False)
        
        print(f"    ❌ Runtime Exception: {e}")
        print(f"    📊 Exception report saved to: {report_path}")
        return False, [str(e)]


def run_analysis_mode(legacy_files, input_dir, specs_dir):
    """Runs only the Specification Generator for all files."""
    print(f"\n📊 STARTING ANALYSIS MODE")
    
    # 1. Run Project Scanner
    scanner = ProjectScanner(input_dir)
    project_context = scanner.scan()
    
    print(f"   Generating specifications for {len(legacy_files)} files...\n")
    
    # Create simple workflow for analysis
    workflow = StateGraph(AgentState)
    workflow.add_node("classifier", classifier_node)
    workflow.add_node("spec_generator", specification_generator_node)
    workflow.set_entry_point("classifier")
    workflow.add_edge("classifier", "spec_generator")
    workflow.add_edge("spec_generator", END)
    app = workflow.compile()

    os.makedirs(specs_dir, exist_ok=True)
    
    generated_specs = []

    for filepath in legacy_files:
        rel_path = os.path.relpath(filepath, input_dir)
        print(f"🔍 Analyzing: {rel_path}...")
        
        initial_state = {
            "legacy_filepath": filepath,
            "project_context": project_context  # Pass context to agents
        }
        try:
            result = app.invoke(initial_state)
            spec = result.get("specification")
            
            if spec:
                # Save spec file
                base_name = os.path.splitext(rel_path)[0]
                spec_filename = f"{base_name}.spec.md"
                spec_path = os.path.join(specs_dir, spec_filename)
                os.makedirs(os.path.dirname(spec_path), exist_ok=True)
                
                with open(spec_path, "w", encoding="utf-8") as f:
                    f.write(spec)
                print(f"    ✅ Spec saved: {spec_path}\n")
                generated_specs.append(spec_path)
            else:
                print(f"    ❌ Failed to generate spec.\n")
                
        except Exception as e:
            print(f"    ❌ Error: {e}\n")

    # Generate Consolidated Project Report
    if generated_specs:
        generate_project_summary(project_context, generated_specs, specs_dir)

    print(f"✨ Analysis Complete! Check {specs_dir} for specifications.")


def handle_input_source(input_arg):
    """Handles directory or zip file input."""
    if not input_arg:
        return DEFAULT_INPUT_DIR

    if os.path.isdir(input_arg):
        return input_arg
    
    if zipfile.is_zipfile(input_arg):
        print(f"📦 Detected ZIP file: {input_arg}")
        print(f"   Extracting to {TEMP_DIR}...")
        
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR, exist_ok=True)
        
        with zipfile.ZipFile(input_arg, 'r') as zip_ref:
            zip_ref.extractall(TEMP_DIR)
            
        print(f"   ✅ Extraction complete.")
        return TEMP_DIR
    
    print(f"❌ Error: Input '{input_arg}' is not a valid directory or zip file.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Assembly Line Modernizer")
    parser.add_argument("--config", help="Path to configuration file", default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--mode", choices=["analyze", "modernize"], help="Override mode from config")
    parser.add_argument("--input", help="Override input path from config")
    args = parser.parse_args()

    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ CRITICAL: GOOGLE_API_KEY is missing. Check .env file.")
        return

    # 1. Load Config
    config = load_config(args.config)
    
    # 2. Determine Settings (CLI overrides Config overrides Defaults)
    mode = args.mode or config.get("app", {}).get("mode", "modernize")
    input_arg = args.input or config.get("input", {}).get("path", DEFAULT_INPUT_DIR)
    
    DEFAULT_REPORTS_DIR = "workspace/output_reports"
    output_config = config.get("output", {})
    specs_dir = output_config.get("specs_dir", DEFAULT_SPECS_DIR)
    modern_dir = output_config.get("modern_dir", DEFAULT_OUTPUT_DIR)
    reports_dir = output_config.get("reports_dir", DEFAULT_REPORTS_DIR)
    final_zip_path = output_config.get("final_zip_path", "workspace/modernized_app.zip")

    # 3. Handle Input
    input_dir = handle_input_source(input_arg)

    # Ensure directories exist
    if not os.path.exists(input_dir):
        print(f"❌ Input directory '{input_dir}' not found. Creating it...")
        os.makedirs(input_dir, exist_ok=True)
        return

    # Discovery Phase
    legacy_files = []
    supported_extensions = (".java", ".xhtml", ".jsp", ".js", ".xml", ".properties")
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(supported_extensions):
                legacy_files.append(os.path.join(root, file))

    if not legacy_files:
        print(f"⚠️  No supported files found in '{input_dir}'. Please add files to process.")
        return

    # Mode Selection
    if mode == "analyze":
        run_analysis_mode(legacy_files, input_dir, specs_dir)
        return

    # Modernization Mode (Default)
    print(f"🚀 STARTING MODERNIZATION MODE")
    
    # 1. Run Project Scanner (New)
    scanner = ProjectScanner(input_dir)
    project_context = scanner.scan()
    
    print(f"🔍 Found {len(legacy_files)} files. Starting Batch Migration...\n")

    # Initialize the Graph
    app = build_workflow()

    # Execution Phase
    stats = {"success": 0, "failed": 0, "details": []}

    for filepath in legacy_files:
        # Pass project_context and output_dir to process_file
        success, errors = process_file(app, filepath, input_dir, modern_dir, reports_dir, project_context)

        if success:
            stats["success"] += 1
            stats["details"].append((filepath, "Success"))
        else:
            stats["failed"] += 1
            stats["details"].append((filepath, f"Failed: {errors}"))

        # Optional: Sleep briefly to respect API rate limits
        time.sleep(1)

    # Final Report
    print("\n" + "=" * 50)
    print(f"🏁 BATCH MIGRATION COMPLETE")
    print(f"   Total Processed: {len(legacy_files)}")
    print(f"   Success: {stats['success']}")
    print(f"   Failed:  {stats['failed']}")
    print("=" * 50)

    if stats["failed"] > 0:
        print("\nFailures:")
        for path, reason in stats["details"]:
            if "Failed" in reason:
                print(f" - {os.path.basename(path)}: {reason}")
                
    # Zip Output if Input was Zip
    if zipfile.is_zipfile(input_arg):
        print(f"\n📦 Packaging output into ZIP...")
        # Remove .zip extension if present in final_zip_path for shutil.make_archive
        base_name = os.path.splitext(final_zip_path)[0]
        shutil.make_archive(base_name, 'zip', modern_dir)
        print(f"   ✅ Created: {base_name}.zip")


if __name__ == "__main__":
    main()
