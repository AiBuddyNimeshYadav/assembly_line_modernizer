import re


def analyze_java_code(content: str):
    """
    A heuristic parser to identify component types and dependencies
    without requiring a full JVM environment.
    """
    results = {
        "type": "unknown",
        "dependencies": [],
    }

    # 1. Detect Type based on Annotations
    if "@ManagedBean" in content or "@Controller" in content:
        results["type"] = "backend"
    elif "@Entity" in content:
        results["type"] = "model"
    elif "interface " in content:
        results["type"] = "backend"

    # 2. Detect Dependencies (e.g., 'private UserService userService;')
    # Regex looks for: private [Type] [camelCaseName];
    dependency_pattern = r'private\s+([A-Z][a-zA-Z0-9]+)\s+[a-z][a-zA-Z0-9]+;'
    matches = re.findall(dependency_pattern, content)
    results["dependencies"] = list(set(matches))

    return results