# Assembly Line Modernizer - User Guide

## Introduction
The Assembly Line Modernizer is a tool designed to automate the migration of legacy Java applications (specifically JSF/PrimeFaces) to a modern stack (Spring Boot/React). It uses a pipeline of AI agents to analyze, plan, generate, and validate code.

## Installation

1.  **Clone the Repository**
2.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up API Key**:
    - Create a `.env` file in the root directory.
    - Add your Google Gemini API key: `GOOGLE_API_KEY=AIzaSy...`

## Configuration (`config.yaml`)

The `config.yaml` file controls the behavior of the tool.

```yaml
app:
  mode: "modernize"  # Options: "modernize", "analyze"

input:
  type: "directory"  # Options: "directory", "zip"
  path: "workspace/input_legacy" # Path to your legacy code

output:
  modern_dir: "workspace/output_modern"   # Where generated code goes
  reports_dir: "workspace/output_reports" # Where JSON reports go
  specs_dir: "workspace/output_specs"     # Where analysis specs go
  final_zip_path: "workspace/modernized_app.zip" # For ZIP output
```

## Modes of Operation

### 1. Modernize Mode (`--mode modernize`)
This is the default mode. It performs the actual code migration.
- **Input**: Legacy source files.
- **Output**: Modernized source files in `modern_dir` and JSON reports in `reports_dir`.
- **Process**:
    1.  **Scan**: Understands project context.
    2.  **Classify**: Identifies file type.
    3.  **Plan**: Creates a migration checklist.
    4.  **Generate**: Writes new code.
    5.  **Validate**: Checks for errors and retries if necessary.

### 2. Analyze Mode (`--mode analyze`)
Use this mode to understand the legacy codebase without modifying it.
- **Input**: Legacy source files.
- **Output**: Markdown specifications in `specs_dir` and a consolidated `project_summary.md`.
- **Process**:
    1.  **Scan**: Understands project context.
    2.  **Classify**: Identifies file type.
    3.  **Spec Gen**: Generates a detailed technical specification for each file.
    4.  **Summarize**: Aggregates all specs into a project-level report.

## Running the Tool

### Basic Usage
Run with default configuration:
```bash
python main.py --config config.yaml
```

### Overriding Configuration via CLI
You can override config settings using command-line arguments:

- **Change Mode**:
  ```bash
  python main.py --mode analyze
  ```

- **Change Input Directory**:
  ```bash
  python main.py --input /path/to/my/legacy/app
  ```

- **Process a ZIP File**:
  ```bash
  python main.py --input /path/to/legacy_app.zip
  ```

## Interpreting Outputs

### Modernized Code (`workspace/output_modern`)
This directory mirrors your input directory structure but contains the modernized files.
- `.java` files are converted to Spring Boot (e.g., `@RestController`).
- `.xhtml` files are converted to React (`.tsx`).
- `build.xml` is converted to `build.gradle`.

### Reports (`workspace/output_reports`)
For every processed file, a `.report.json` is generated. It contains:
- **Status**: `success` or `failed`.
- **Classification**: What the AI thought the file was.
- **Plan**: The steps the AI decided to take.
- **Validation**: Any errors found and fixed during the process.

### Specifications (`workspace/output_specs`)
(Only in Analyze Mode)
- **`[filename].spec.md`**: Detailed analysis of a single file.
- **`project_summary.md`**: A high-level overview of the entire project's architecture and modernization complexity.

## Troubleshooting

- **Rate Limits**: If you see `429 RESOURCE_EXHAUSTED`, the tool will automatically retry. If it fails repeatedly, wait a few minutes and try again.
- **Validation Failures**: If a file fails validation 3 times, check the `report.json` to see what errors were found. You may need to adjust the prompt or manually fix the file.
- **Missing Files**: Ensure your input path is correct and contains supported file extensions (`.java`, `.xhtml`, `.xml`, etc.).
