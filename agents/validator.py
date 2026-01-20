from core.state import AgentState

def validator_node(state: AgentState):
    print(f"⚖️  [Validator] Reviewing Code...")
    
    code = state.get("modern_code", "")
    file_type = state.get("file_type", "unknown")
    errors = []

    # Common check: Empty code
    if not code or len(code) < 10:
        errors.append("Code generation failed or was empty.")
        print(f"    ❌ REJECTED. Errors: {errors}")
        return {"compilation_errors": errors, "status": "retry"}

    # FILE TYPE SPECIFIC VALIDATION
    
    # 1. BACKEND JAVA VALIDATION
    if file_type == "backend":
        # No JSF imports allowed
        if "javax.faces" in code:
            errors.append("Found legacy 'javax.faces' import - must be removed.")
        
        # No JSF annotations
        if "@ManagedBean" in code or "@ViewScoped" in code or "@SessionScoped" in code:
            errors.append("Found JSF annotations (@ManagedBean, @ViewScoped, etc.) - use Spring annotations.")
        
        # Should have Spring annotations (basic check)
        has_spring = any(x in code for x in ["@RestController", "@Service", "@Component", "@Repository"])
        if not has_spring:
            errors.append("Missing Spring annotations (@RestController, @Service, etc.).")
    
    # 2. JSF VIEW → REACT VALIDATION
    elif file_type == "jsf_view":
        # No JSF/PrimeFaces tags
        if any(tag in code for tag in ["<h:form", "<p:dataTable", "<p:", "<h:", "xmlns:p=", "xmlns:h="]):
            errors.append("Found JSF/PrimeFaces tags - must convert to React components.")
        
        # Should have React imports
        if "import React" not in code and "import {" not in code:
            errors.append("Missing React imports - this should be a React component.")
        
        # Should use functional component pattern
        if "export default" not in code and "export const" not in code:
            errors.append("Missing React component export.")
    
    # 3. FRONTEND JAVASCRIPT → TYPESCRIPT
    elif file_type == "frontend_js":
        # Basic TypeScript check (should have type annotations or interfaces)
        has_typescript = any(x in code for x in ["interface ", "type ", ": string", ": number", ": boolean"])
        if not has_typescript:
            errors.append("Code should be TypeScript with type annotations, not plain JavaScript.")
    
    # 4. ANT → GRADLE VALIDATION
    elif file_type == "build_ant":
        # Should have Gradle syntax
        if "plugins {" not in code and "plugins(" not in code:
            errors.append("Missing Gradle plugins block - this doesn't look like a valid Gradle file.")
        
        # Check for Spring Boot plugin (if applicable)
        if "spring" in state.get("legacy_content", "").lower():
            if "spring-boot" not in code.lower():
                errors.append("Original build had Spring - modernized Gradle should include Spring Boot plugin.")
    
    # 5. MAVEN POM VALIDATION
    elif file_type == "build_maven":
        # Should still have XML structure
        if "<project" not in code or "</project>" not in code:
            errors.append("Invalid Maven POM structure - missing root <project> element.")
    
    # 6. SECURITY CONFIG VALIDATION
    elif file_type == "security_config":
        # Should have Spring Security imports
        if "import org.springframework.security" not in code:
            errors.append("Missing Spring Security imports.")
        
        # Should have SecurityFilterChain bean (modern pattern)
        if "SecurityFilterChain" not in code:
            errors.append("Should use SecurityFilterChain bean pattern (Spring Security 6 style).")
        
        # No XML-style configuration
        if "<security" in code or "web.xml" in code:
            errors.append("Should be Java configuration, not XML.")

    # Final verdict
    if errors:
        print(f"    ❌ REJECTED. Errors: {errors}")
        return {"compilation_errors": errors, "status": "retry"}
    else:
        print(f"    ✅ APPROVED. Code meets standards.")
        return {"compilation_errors": None, "status": "complete"}
