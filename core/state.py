from typing import TypedDict, List, Optional, Literal


class AgentState(TypedDict):
    # Inputs
    legacy_filepath: str
    legacy_content: str

    # Classification & Metadata
    file_type: Literal[
        "backend",           # Java backend code
        "jsf_view",          # JSF XHTML views
        "primefaces_component",  # PrimeFaces-heavy components
        "frontend_js",       # Legacy JavaScript
        "build_ant",         # Ant build.xml
        "build_maven",       # Maven pom.xml
        "security_config",   # web.xml, security configs
        "config",            # Other configs
        "unknown"
    ]
    target_extension: str  # e.g., ".java", ".tsx", ".gradle", ".xml"
    detected_dependencies: List[str]
    
    # Frontend-specific
    frontend_framework: Optional[Literal["react", "nextjs"]]  # Target frontend framework
    ui_library: Optional[Literal["primereact", "mui"]]  # Target UI library
    detected_components: Optional[List[str]]  # PrimeFaces components found (e.g., ["p:dataTable", "p:dialog"])
    converted_components: Optional[List[str]]  # React component names created

    # Workflow Data
from typing import TypedDict, List, Optional, Literal


class AgentState(TypedDict):
    # Inputs
    legacy_filepath: str
    legacy_content: str

    # Classification & Metadata
    file_type: Literal[
        "backend",           # Java backend code
        "jsf_view",          # JSF XHTML views
        "primefaces_component",  # PrimeFaces-heavy components
        "frontend_js",       # Legacy JavaScript
        "build_ant",         # Ant build.xml
        "build_maven",       # Maven pom.xml
        "security_config",   # web.xml, security configs
        "config",            # Other configs
        "unknown"
    ]
    target_extension: str  # e.g., ".java", ".tsx", ".gradle", ".xml"
    detected_dependencies: List[str]
    
    # Frontend-specific
    frontend_framework: Optional[Literal["react", "nextjs"]]  # Target frontend framework
    ui_library: Optional[Literal["primereact", "mui"]]  # Target UI library
    detected_components: Optional[List[str]]  # PrimeFaces components found (e.g., ["p:dataTable", "p:dialog"])
    converted_components: Optional[List[str]]  # React component names created

    # Workflow Data
    build_priority: int
    is_ready_to_process: bool

    # Agent Outputs
    modernization_plan: Optional[str]  # From Planner
    modern_code: Optional[str]  # From Worker
    iteration_count: int
    compilation_errors: Optional[List[str]]  # From Validator
    specification: Optional[str]  # From SpecGenerator

    # Flow Control
    status: Literal["pending", "in_progress", "complete", "failed", "retry", "blocked"]