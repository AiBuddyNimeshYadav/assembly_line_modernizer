# Quick Start Guide - Full Stack Modernization

## 🚀 Ready to Test!

I've created sample legacy files for you to test the modernization pipeline:

### Sample Files Created:

1. **`workspace/input_legacy/UserController.java`**
   - Legacy JSF Managed Bean
   - Uses `@ManagedBean`, `@ViewScoped`
   - Old Date API, JSF navigation
   - Will transform to → Spring Boot REST Controller

2. **`workspace/input_legacy/users.xhtml`**
   - JSF/PrimeFaces view
   - Components: DataTable, Dialog, CommandButton, InputText
   - Will transform to → React + TypeScript + PrimeReact

---

## 📝 How to Run

### 1. Make sure `.env` file exists with your API key:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 2. Run the modernization:
```bash
python main.py --config config.yaml
```
*(Or just `python main.py` to use defaults)*

### 3. Watch the pipeline work:
```
🚀 STARTING MODERNIZATION MODE
🔍 [ProjectScanner] Scanning project structure...
    ✅ Identified Tech Stack: JSF, Java, Maven

🔄 Processing: UserController.java...

🔍 [Classifier] Classifying: UserController.java...
    Type: BACKEND | Target: .java

📋 [DependencyCheck] Checking dependencies...
    ✅ Green light

📝 [Architect] Drafting Modernization Plan...
    ✅ Plan created

🔨 [CodeGenerator] Generating Code with Gemini...
    Using prompt: backend_java21_spring.txt

⚖️  [Validator] Reviewing Code...
    ✅ APPROVED

✅ Success! Saved to: workspace/output_modern/UserController.java
```

---

## 🎯 Expected Outputs

### Backend: `UserController.java` will become:
- `@RestController` with REST endpoints
- Constructor injection with Lombok
- Java 21 Records for DTOs
- `LocalDateTime` instead of `Date`
- `ResponseEntity<T>` return types
- Spring Data JPA patterns

### Frontend: `users.xhtml` will become `users.tsx`:
- React functional component
- TypeScript interfaces
- PrimeReact components (DataTable, Dialog, Button)
- `useState` and `useEffect` hooks
- API calls with axios/fetch
- Modern TypeScript patterns

---

## 📊 What Each Agent Does

| Agent | Role | What it does for UserController.java |
|-------|------|-------------------------------------|
| 🔍 **ProjectScanner** | Context Builder | Scans whole project to find it's a JSF app |
| 🔍 **Classifier** | Classifier | Detects it's a JSF backend file |
| 📋 **DependencyCheck** | Dependency Manager | Checks if dependencies are ready |
| 📝 **Architect** | Architect | Creates Java 8→21 + JSF→Spring Boot roadmap |
| 🔨 **CodeGenerator** | Code Generator | Transforms using Gemini + specialized prompt |
| ⚖️ **Validator** | Quality Control | Validates no JSF imports, has Spring annotations |

---

## 🧪 Test Different Scenarios

Try adding these files to test other layers:

### Test Ant → Gradle:
Create `workspace/input_legacy/build.xml`:
```xml
<project name="MyApp" default="compile">
    <target name="compile">
        <javac srcdir="src" destdir="build"/>
    </target>
</project>
```

### Test Security Config:
Create `workspace/input_legacy/web.xml`:
```xml
<web-app>
    <security-constraint>
        <web-resource-collection>
            <url-pattern>/admin/*</url-pattern>
        </web-resource-collection>
        <auth-constraint>
            <role-name>ADMIN</role-name>
        </auth-constraint>
    </security-constraint>
</web-app>
```

---

## 🐛 Troubleshooting

### Error: "GOOGLE_API_KEY is missing"
- Create `.env` file in project root
- Add: `GOOGLE_API_KEY=your_key_here`

### Error: Module not found
```bash
pip install -r requirements.txt
```

### No files found
- Make sure files are in `workspace/input_legacy/`
- Check file extensions match: `.java`, `.xhtml`, `.jsp`, `.js`, `.xml`

---

## 📈 Next Steps

1. **Run the test** with the sample files
2. **Review the output** in `workspace/output_modern/`
3. **Add your real legacy code** to `workspace/input_legacy/`
4. **Iterate** - The validator will retry up to 3 times if validation fails

---

## 🎉 You're Ready!

Your full-stack modernization pipeline is complete and ready to transform:
- ✅ Java 8 → Java 21
- ✅ JSF → Spring Boot 3
- ✅ PrimeFaces → React + PrimeReact
- ✅ Ant → Gradle
- ✅ web.xml → Spring Security 6

Just run `python main.py` and watch the magic happen! 🚀
