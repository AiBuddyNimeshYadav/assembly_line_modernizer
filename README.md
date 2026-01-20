# Assembly Line Modernization Agent

An AI-powered multi-agent system that automatically modernizes legacy Java/JSF applications to modern Spring Boot + React stack using Google Gemini.

## Supported Migrations

| Layer | From (Legacy) | To (Modern) |
|-------|---------------|-------------|
| **Language** | Java 8 | Java 21 LTS |
| **Framework** | JSF 2.1 / Managed Beans | Spring Boot 3.x / REST APIs |
| **Frontend** | JSF XHTML / PrimeFaces | React (TypeScript) + PrimeReact |
| **Build** | Ant (`build.xml`) | Gradle |
| **Build** | Maven (Legacy) | Maven (Modern with Spring Boot) |
| **Security** | `web.xml` config | Spring Security 6 (Java Config) |
| **JavaScript** | Legacy JS | Modern TypeScript |

## Features

✅ **Multi-Layer Modernization**: Handles backend, frontend, build files, and security configs  
✅ **Project-Aware**: Scans the entire project context (tech stack, dependencies) before processing  
✅ **Intelligent Classification**: Detects PrimeFaces components and file types automatically  
✅ **AI-Powered**: Uses Google Gemini with specialized prompts for each transformation  
✅ **Self-Correcting**: Validation loops ensure quality output (up to 3 retries)  
✅ **Batch Processing**: Processes entire directory structures recursively  
✅ **Structure Preservation**: Maintains original directory hierarchy

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Configure Settings**:
   The tool uses `config.yaml` for configuration. You can modify it to set your input/output paths and preferred mode.
   ```yaml
   app:
     mode: "modernize" # or "analyze"
   input:
     type: "directory" # or "zip"
     path: "workspace/input_legacy"
   output:
     modern_dir: "workspace/output_modern"
     reports_dir: "workspace/output_reports"
   ```

4. **Prepare Legacy Code**:
   - Place your legacy files in the configured input path (default: `workspace/input_legacy/`)
   - Or point the `input.path` in `config.yaml` to your existing project directory or ZIP file.

5. **Run Migration**:
   ```bash
   python main.py --config config.yaml
   ```
   *Note: CLI arguments like `--mode` or `--input` override config settings.*

6. **Review Output**:
   - **Modernized Code**: `workspace/output_modern/` (or configured path)
   - **Reports**: `workspace/output_reports/` (JSON details)
   - **Project Summary**: `workspace/output_specs/project_summary.md` (in Analysis Mode)
   - **ZIP Output**: `workspace/modernized_app.zip` (if input was a ZIP)

## Architecture
The system uses a multi-agent pipeline:

1. **ProjectScanner**: Scans the entire project first to identify tech stack, packages, and global dependencies.
2. **Classifier**: Identifies file types and detects components (e.g., PrimeFaces tags).
3. **DependencyCheck**: Validates if the file is ready for processing.
4. **Architect**: Creates a detailed modernization roadmap based on project context.
5. **CodeGenerator**: Generates modernized code using Gemini with specialized prompts.
6. **Validator**: Validates output against quality rules and triggers retries if needed.
7. **ProjectSummarizer**: (Analysis Mode) Aggregates all file specs into a comprehensive project report.

## Examples

**JSF Managed Bean → Spring REST Controller**:
- Input: `@ManagedBean` with `@ViewScoped`
- Output: `@RestController` with constructor injection, Java 21 features

**PrimeFaces XHTML → React Component**:
- Input: `<p:dataTable>`, `<p:dialog>`
- Output: React functional component with PrimeReact, TypeScript interfaces

**Ant build.xml → Gradle**:
- Input: Ant targets and dependencies
- Output: Modern `build.gradle` with Spring Boot plugin
