# Assembly Line Modernizer - Live Demo Script

## 🎯 Objective
Demonstrate the automated modernization of a legacy Java/JSF application to a modern Spring Boot/React stack using the AI Assembly Line.

## 🕒 Duration
Approx. 10-15 Minutes

## 🛠️ Prerequisites
- [ ] Python environment active (`.venv`)
- [ ] `GOOGLE_API_KEY` set in `.env`
- [ ] `config.yaml` configured for "modernize" mode
- [ ] Clean workspace: `workspace/output_modern` and `workspace/output_reports` should be empty (or deleted).
- [ ] Legacy sample files present in `workspace/input_legacy`.

---

## 🎬 Act 1: The Setup (2 Minutes)

**Narrator**: "Welcome. Today we're tackling the challenge of legacy modernization. We have a legacy JSF application that needs to be migrated to Spring Boot and React. Instead of rewriting it manually, we'll use our AI Assembly Line."

**Action 1**: Show the Legacy Code.
- Open `workspace/input_legacy/UserController.java`.
- **Highlight**: `@ManagedBean`, `@ViewScoped`, `java.util.Date`, `FacesContext`.
- **Say**: "This is a typical JSF Managed Bean. It's tightly coupled to the web container and uses outdated Java APIs."

**Action 2**: Show the Configuration.
- Open `config.yaml`.
- **Say**: "We configure the system here. We're running in 'modernize' mode, pointing to our legacy directory."

---

## 🎬 Act 2: The Execution (5 Minutes)

**Narrator**: "Now, let's start the assembly line."

**Action 3**: Run the Tool.
- Terminal: `python main.py --config config.yaml`
- **Say**: "I'm starting the process. Watch the logs."

**Action 4**: Narrate the Agent Flow (while tool runs).
- **ProjectScanner**: "First, the Scanner analyzes the whole project structure to understand the tech stack."
- **Classifier**: "Now it's classifying `UserController.java`. It knows it's a Backend file."
- **Architect**: "The Architect is drafting a plan: Replace ManagedBean with RestController, update Date to LocalDateTime..."
- **CodeGenerator**: "The CodeGenerator is now writing the Spring Boot code."
- **Validator**: "Finally, the Validator checks the code. If it finds any JSF imports left, it will reject it and ask for a fix."

---

## 🎬 Act 3: The Reveal (5 Minutes)

**Narrator**: "The process is complete. Let's see what we built."

**Action 5**: Show the Modernized Code.
- Open `workspace/output_modern/UserController.java`.
- **Highlight**:
    - `@RestController` (replaced `@ManagedBean`)
    - `LocalDateTime` (replaced `Date`)
    - Constructor Injection (Modern Spring pattern)
    - `ResponseEntity` (RESTful response)
- **Say**: "It's not just a translation; it's a modernization. We have a clean, stateless REST controller."

**Action 6**: Show the Report.
- Open `workspace/output_reports/UserController.report.json`.
- **Show**: The `modernization_plan` and `classification` sections.
- **Say**: "We also get a full audit trail of what decisions were made."

---

## 🎬 Act 4: Analysis Mode (Optional - 3 Minutes)

**Narrator**: "What if we just want to estimate the work first?"

**Action 7**: Run Analysis Mode.
- Terminal: `python main.py --mode analyze`
- **Say**: "In Analysis mode, we don't write code. We generate specifications."

**Action 8**: Show the Spec.
- Open `workspace/output_specs/UserController.spec.md`.
- **Say**: "This gives us a detailed technical breakdown of the legacy file, perfect for planning sprints."

---

## 🏁 Conclusion
**Narrator**: "We've successfully transformed legacy code into modern, cloud-native architecture in minutes, not days. This is the power of the Assembly Line Modernizer."
