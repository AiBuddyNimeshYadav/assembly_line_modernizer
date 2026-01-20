import os
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any

class ProjectScanner:
    """
    Scans the entire codebase to build a high-level context of the project.
    Identifies dependencies, package structure, and shared resources.
    """

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.context = {
            "project_name": os.path.basename(root_dir),
            "tech_stack": [],
            "dependencies": [],
            "modules": [],
            "packages": [],
            "file_stats": {}
        }

    def scan(self) -> Dict[str, Any]:
        """Performs the scan and returns the project context."""
        print(f"🔍 [ProjectScanner] Scanning project structure in: {self.root_dir}")
        
        self._scan_file_types()
        self._scan_build_files()
        self._scan_java_packages()
        
        # Deduplicate and sort
        self.context["tech_stack"] = sorted(list(set(self.context["tech_stack"])))
        self.context["dependencies"] = sorted(list(set(self.context["dependencies"])))
        self.context["packages"] = sorted(list(set(self.context["packages"])))
        
        print(f"    ✅ Identified Tech Stack: {', '.join(self.context['tech_stack'])}")
        print(f"    ✅ Found {len(self.context['dependencies'])} global dependencies")
        print(f"    ✅ Found {len(self.context['packages'])} Java packages")
        
        return self.context

    def _scan_file_types(self):
        """Counts files by extension and infers tech stack."""
        stats = {}
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                stats[ext] = stats.get(ext, 0) + 1
                
                # Infer tech stack
                if ext == ".java": self.context["tech_stack"].append("Java")
                elif ext in [".js", ".jsx"]: self.context["tech_stack"].append("JavaScript")
                elif ext in [".ts", ".tsx"]: self.context["tech_stack"].append("TypeScript")
                elif ext == ".xhtml": self.context["tech_stack"].append("JSF")
                elif ext == ".jsp": self.context["tech_stack"].append("JSP")
                elif ext == ".xml" and file == "pom.xml": self.context["tech_stack"].append("Maven")
                elif ext == ".xml" and file == "build.xml": self.context["tech_stack"].append("Ant")
                elif ext == ".gradle": self.context["tech_stack"].append("Gradle")
        
        self.context["file_stats"] = stats

    def _scan_build_files(self):
        """Parses build files to find dependencies."""
        # Maven
        pom_path = os.path.join(self.root_dir, "pom.xml")
        if os.path.exists(pom_path):
            try:
                tree = ET.parse(pom_path)
                root = tree.getroot()
                # Handle namespaces if present, but keep it simple for now
                ns = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
                # Try with and without namespace
                deps = root.findall(".//dependency") or root.findall(".//mvn:dependency", ns)
                
                for dep in deps:
                    group = dep.find("groupId")
                    artifact = dep.find("artifactId")
                    version = dep.find("version")
                    
                    g = group.text if group is not None else ""
                    a = artifact.text if artifact is not None else ""
                    v = version.text if version is not None else ""
                    
                    if g and a:
                        self.context["dependencies"].append(f"{g}:{a}:{v}")
            except Exception as e:
                print(f"    ⚠️  Error parsing pom.xml: {e}")

        # Ant (build.xml) - simple regex or parsing could go here
        # For now, we rely on file type detection for Ant

    def _scan_java_packages(self):
        """Finds Java packages by reading the package declaration."""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".java"):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                if line.strip().startswith("package "):
                                    pkg = line.strip().replace("package ", "").replace(";", "")
                                    self.context["packages"].append(pkg)
                                    break
                    except:
                        pass
