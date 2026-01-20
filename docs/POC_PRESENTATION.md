# Assembly Line Modernizer - Proof of Concept

## 1. Executive Summary
The **Assembly Line Modernizer** is an autonomous, multi-agent AI system designed to accelerate the migration of legacy Java/JSF applications to modern cloud-native stacks (Spring Boot + React). By mimicking a factory assembly line, specialized AI agents handle distinct phases of modernization—from analysis and planning to code generation and quality assurance.

## 2. The Challenge
Modernizing legacy monolithic applications is:
- **Time-Consuming**: Manual rewriting takes months or years.
- **Error-Prone**: Human error in translating logic.
- **Complex**: Deep dependencies and outdated frameworks (JSF, Ant, XML hell).
- **Costly**: High resource requirement for senior engineers.

## 3. The Solution: AI Assembly Line
We treat code migration as a manufacturing process.
- **Input**: Legacy Source Code (Java 8, JSF, Ant)
- **Process**: Sequential Multi-Agent Workflow
- **Output**: Modern Source Code (Java 21, Spring Boot, React, Gradle)

### Key Differentiators
- **Project-Aware Context**: Unlike simple chatbots, our `ProjectScanner` understands the entire project structure, dependencies, and tech stack before touching a single file.
- **Self-Healing**: The `Validator` agent compiles and checks code, sending it back to the `CodeGenerator` for fixes if issues are found.
- **Configuration-Driven**: Fully customizable via `config.yaml`.

## 4. System Architecture

### The Agents
1.  **🔍 ProjectScanner**: The "Site Surveyor". Scans the repo to build a global context map.
2.  **🔍 Classifier**: The "Sorter". Identifies file types (Backend, UI, Config) and detects libraries (PrimeFaces, Hibernate).
3.  **📋 DependencyCheck**: The "Gatekeeper". Ensures prerequisites are met.
4.  **📝 Architect**: The "Planner". Drafts a step-by-step migration plan (e.g., "Replace @ManagedBean with @RestController").
5.  **🔨 CodeGenerator**: The "Builder". Writes the actual code using Google Gemini 2.5 Flash.
6.  **⚖️ Validator**: The "Inspector". Reviews code for compilation errors, forbidden patterns, and best practices.

### The Workflow
`Legacy Code` -> `Scan` -> `Classify` -> `Plan` -> `Generate` -> `Validate` -> `Modern Code`

## 5. Modes of Operation
1.  **Analyze Mode**: Non-destructive. Generates detailed `.spec.md` specifications and a `project_summary.md` report. Useful for estimation and understanding.
2.  **Modernize Mode**: Active migration. Produces production-ready code in `workspace/output_modern`.

## 6. Demonstration Scenarios

### Scenario A: Backend Migration
- **Input**: `UserController.java` (JSF Managed Bean, Date API)
- **Transformation**:
    - `@ManagedBean` -> `@RestController`
    - `Date` -> `LocalDateTime`
    - Manual Getters/Setters -> Lombok `@Data`
- **Result**: Clean, stateless Spring Boot controller.

### Scenario B: Frontend Migration
- **Input**: `users.xhtml` (PrimeFaces `p:dataTable`)
- **Transformation**:
    - XML Tags -> React Components (`<DataTable>`)
    - EL Expressions `#{bean.val}` -> React State & Props
- **Result**: Responsive React TypeScript component.

## 7. Configuration & Extensibility
The system is controlled via `config.yaml`:
```yaml
app:
  mode: "modernize"
input:
  type: "directory"
  path: "workspace/legacy_app"
output:
  modern_dir: "workspace/modern_app"
```

## 8. Future Roadmap
- **Graph-Based Dependency Resolution**: Process files in topological order (Entities -> Repos -> Services -> Controllers).
- **Integration Tests**: Auto-generate JUnit/Jest tests for the new code.
- **Dockerization**: Auto-generate `Dockerfile` and `docker-compose.yml` for the modernized app.
