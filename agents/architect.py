import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from core.state import AgentState


def architect_node(state: AgentState):
    """
    Creates a detailed modernization plan based on file type and detected patterns.
    Supports multi-layer modernization across all technology stacks.
    """
    print("📝 [Architect] Drafting Modernization Plan...")

    file_type = state.get("file_type", "unknown")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("    ⚠️  WARNING: GOOGLE_API_KEY missing - skipping planning")
        return {"modernization_plan": "Skip planning - no API key"}
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )
    except Exception as e:
        print(f"    ❌ Error initializing AI: {e}")
        return {"modernization_plan": f"Error: {e}"}

    # Select prompt based on file type
    system_prompt = get_planning_prompt(file_type, state)
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=state['legacy_content'])
    ])

    print(f"    ✅ Plan created ({len(response.content)} chars)")
    return {"modernization_plan": response.content}


def get_planning_prompt(file_type: str, state: AgentState) -> str:
    """
    Returns specialized planning prompt based on file type and migration layer.
    """
    
    # BACKEND JAVA MODERNIZATION PLAN
    if file_type == "backend":
        return """You are a Senior Java Architect specializing in legacy modernization.

Analyze the provided Legacy Java code and create a detailed Modernization Plan.

TARGET MODERNIZATION:
- Language: Java 8 → Java 21 LTS
- Framework: JSF 2.1 / Managed Beans → Spring Boot 3.x REST APIs
- Server: WebLogic/JBoss → Embedded Tomcat (containerized)
- Security: Container managed → Spring Security 6 (OAuth2/OIDC)

REQUIRED CHANGES:
1. **Dependency Injection**
   - Replace @ManagedBean → @RestController / @Service / @Repository
   - Replace @ViewScoped / @SessionScoped → Remove (stateless REST)
   - Use Constructor Injection with Lombok @RequiredArgsConstructor

2. **Package Migration**
   - Replace javax.* → jakarta.* (Jakarta EE 9+)
   - Remove javax.faces.* imports completely

3. **Java 21 Features**
   - Replace legacy Date/Calendar → java.time.* (LocalDateTime, Instant)
   - Use Records for DTOs (immutable data carriers)
   - Use Pattern Matching for instanceof where applicable
   - Use Text Blocks for multi-line strings
   - Consider Virtual Threads for async operations

4. **Spring Boot Patterns**
   - Add @RestController for API endpoints
   - Return ResponseEntity<T> with proper HTTP status codes
   - Add validation: @Valid, @NotNull, @NotBlank
   - Use Spring Data JPA repositories if database access detected

5. **Code Quality**
   - Use Streams API instead of imperative loops
   - Use Optional instead of null checks
   - Add Lombok annotations: @Data, @Builder, @RequiredArgsConstructor

OUTPUT FORMAT: Markdown checklist with specific code examples."""

    # FRONTEND JSF → REACT MODERNIZATION PLAN
    elif file_type == "jsf_view":
        components = state.get("detected_components", [])
        component_info = f"\n\nDETECTED PRIMEFACES COMPONENTS: {', '.join(components)}" if components else ""
        
        return f"""You are a Frontend Architect specializing in JSF to React migrations.

Analyze the provided JSF/PrimeFaces XHTML view and create a Modernization Plan.

TARGET MODERNIZATION:
- Frontend: JSF / PrimeFaces → React 18+ (TypeScript)
- UI Library: PrimeFaces → PrimeReact
- State Management: Managed Beans → React Hooks + REST APIs
{component_info}

REQUIRED CHANGES:
1. **Component Structure**
   - Convert to React Functional Component with TypeScript
   - Use arrow function syntax
   - Export as default or named export

2. **PrimeFaces → PrimeReact Mapping**
   - <p:dataTable> → <DataTable> from 'primereact/datatable'
   - <p:column> → <Column> from 'primereact/column'
   - <p:inputText> → <InputText> from 'primereact/inputtext'
   - <p:calendar> → <Calendar> from 'primereact/calendar'
   - <p:dialog> → <Dialog> from 'primereact/dialog'
   - <p:button> → <Button> from 'primereact/button'
   - <p:selectOneMenu> → <Dropdown> from 'primereact/dropdown'

3. **State & Data Management**
   - Replace backing bean variables → useState hooks
   - Replace managed bean method calls → REST API calls (axios/fetch)
   - Replace JSF navigation → React Router (useNavigate)
   - Replace AJAX updates → useEffect hooks

4. **Forms & Validation**
   - Use controlled components (value + onChange)
   - Add TypeScript interfaces for form data
   - Implement validation logic or use react-hook-form

5. **Styling**
   - Import PrimeReact theme CSS
   - Use CSS modules or styled-components
   - Ensure responsive design

OUTPUT FORMAT: Markdown checklist with before/after examples."""

    # BUILD SYSTEM MODERNIZATION PLAN
    elif file_type == "build_ant":
        return """You are a Build System Expert specializing in Ant to Gradle migrations.

Analyze the provided Ant build.xml and create a Modernization Plan.

TARGET MODERNIZATION:
- Build: Apache Ant → Gradle 8.x (Groovy DSL)
- Dependency Management: Manual JARs → Maven Central repositories
- Java Version: Target Java 21

REQUIRED CHANGES:
1. **Plugin Configuration**
   - Add java plugin
   - Add Spring Boot Gradle Plugin (if Spring detected)
   - Add io.spring.dependency-management plugin

2. **Dependencies**
   - Convert <fileset> JARs → implementation() declarations
   - Use Spring Boot Starter dependencies
   - Group dependencies by scope (implementation, testImplementation, runtimeOnly)

3. **Tasks**
   - Ant <javac> → Automatically handled by java plugin
   - Ant <jar> → jar or bootJar task
   - Ant <junit> → test task with JUnit 5

4. **Properties**
   - Set sourceCompatibility = '21'
   - Configure group and version
   - Add repository configuration (mavenCentral())

OUTPUT FORMAT: Markdown checklist with Gradle syntax examples."""

    # MAVEN MODERNIZATION PLAN
    elif file_type == "build_maven":
        return """You are a Maven Expert specializing in modernizing legacy POMs.

Analyze the provided legacy pom.xml and create a Modernization Plan.

TARGET MODERNIZATION:
- Build: Legacy Maven → Modern Maven with Spring Boot Parent
- Java Version: Java 8 → Java 21
- Dependencies: Legacy versions → Latest stable versions

REQUIRED CHANGES:
1. **Parent POM**
   - Add spring-boot-starter-parent as parent
   - Set version to 3.2.x or latest

2. **Properties**
   - Set java.version to 21
   - Set project encoding to UTF-8
   - Update dependency versions

3. **Dependencies**
   - Replace javax.* → jakarta.* dependencies
   - Use Spring Boot Starters
   - Update to latest stable versions
   - Remove deprecated dependencies

4. **Plugins**
   - Add spring-boot-maven-plugin
   - Update maven-compiler-plugin to support Java 21
   - Add maven-surefire-plugin for testing

OUTPUT FORMAT: Markdown checklist with XML snippets."""

    # SECURITY CONFIGURATION PLAN
    elif file_type == "security_config":
        return """You are a Security Expert specializing in Spring Security 6.

Analyze the provided web.xml security configuration and create a Modernization Plan.

TARGET MODERNIZATION:
- Security: Container Managed / web.xml → Spring Security 6 Java Config
- Authentication: Basic/Form → OAuth2 / OIDC support
- Authorization: Role-based with modern patterns

REQUIRED CHANGES:
1. **Configuration Class**
   - Create SecurityConfig.java with @Configuration
   - Add @EnableWebSecurity
   - Add @EnableMethodSecurity for method-level security

2. **Security Filter Chain**
   - Use SecurityFilterChain bean pattern
   - Configure with Lambda DSL (modern syntax)
   - Set up HTTP security rules

3. **Authentication**
   - Implement UserDetailsService for user loading
   - Add BCryptPasswordEncoder bean
   - Configure OAuth2/OIDC if needed

4. **Authorization**
   - Map URL patterns to roles
   - Use requestMatchers() instead of deprecated antMatchers()
   - Add CORS configuration if needed

OUTPUT FORMAT: Markdown checklist with Java code examples."""

    # FRONTEND JAVASCRIPT MODERNIZATION
    elif file_type == "frontend_js":
        return """You are a JavaScript/TypeScript Expert.

Analyze the provided legacy JavaScript and create a Modernization Plan.

TARGET MODERNIZATION:
- Language: Legacy JavaScript → Modern TypeScript
- Patterns: Procedural → Functional/Modular
- Type Safety: None → Full TypeScript typing

REQUIRED CHANGES:
1. **TypeScript Conversion**
   - Add type annotations for variables
   - Create interfaces for objects
   - Add return type annotations for functions

2. **Modern JavaScript**
   - Replace var → const/let
   - Use arrow functions
   - Use template literals
   - Use destructuring
   - Use async/await instead of callbacks

3. **Module System**
   - Use ES6 imports/exports
   - Organize into modules

OUTPUT FORMAT: Markdown checklist with code examples."""

    # GENERIC CONFIG FILES
    elif file_type == "config":
        return """You are a Configuration Expert.

Analyze the provided configuration file and suggest modernization improvements.

Focus on:
1. Spring Boot compatibility
2. Modern best practices
3. Security considerations
4. Environment-specific configurations

OUTPUT FORMAT: Markdown checklist."""

    # UNKNOWN/FALLBACK
    else:
        return """You are a Software Modernization Expert.

Analyze the provided code and suggest modernization improvements targeting:
- Latest LTS versions of languages/frameworks
- Modern design patterns
- Best practices for maintainability

OUTPUT FORMAT: Markdown checklist."""