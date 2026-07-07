import os
from typing import List, Dict, Any, Set
from ProjectOS.registry.parser import RegistryParser

class DependencyEngine:
    """Project OS Dependency Resolution Engine (Certified for Stage 6)"""
    
    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.parser = RegistryParser(repo_root)
        
    def build_dependency_graph(self) -> Dict[str, List[str]]:
        capabilities = self.parser.get_capabilities()
        graph = {}
        for cap in capabilities:
            cap_id = cap.get("id")
            if not cap_id:
                continue
            deps = cap.get("dependencies", [])
            # Detect duplicate edges
            graph[cap_id] = sorted(list(set(deps)))
        return graph

    def analyze_dependencies(self):
        """Analyzes all capabilities for strict Stage 6 dependency requirements."""
        capabilities = self.parser.get_capabilities()
        graph = self.build_dependency_graph()
        all_ids = set(graph.keys())
        
        missing_deps = []
        platform_violations = []
        self_deps = []
        
        cap_map = {cap["id"]: cap for cap in capabilities}
        
        for cap_id, deps in graph.items():
            cap = cap_map[cap_id]
            cap_platform = cap.get("platform", "").lower()
            
            for dep in deps:
                # 1. Self dependency
                if dep == cap_id:
                    self_deps.append(cap_id)
                    
                # 2. Unknown / Missing dependency
                if dep not in all_ids:
                    missing_deps.append((cap_id, dep))
                    continue
                    
                # 3. Platform Purity Violation
                dep_cap = cap_map.get(dep)
                if dep_cap:
                    dep_platform = dep_cap.get("platform", "").lower()
                    if cap_platform and dep_platform:
                        # e.g., Platform 1 cannot depend on Platform 10
                        try:
                            cap_num = int("".join(filter(str.isdigit, cap_platform)))
                            dep_num = int("".join(filter(str.isdigit, dep_platform)))
                            if cap_num < dep_num:
                                platform_violations.append((cap_id, dep))
                        except ValueError:
                            pass
                            
        return {
            "missing_dependencies": missing_deps,
            "self_dependencies": self_deps,
            "platform_violations": platform_violations
        }

    def detect_circular_dependencies(self) -> List[List[str]]:
        graph = self.build_dependency_graph()
        visited = set()
        path = []
        cycles = []
        
        def dfs(node: str):
            if node in path:
                cycle_idx = path.index(node)
                cycles.append(path[cycle_idx:] + [node])
                return
            if node in visited:
                return
            visited.add(node)
            path.append(node)
            for neighbor in graph.get(node, []):
                dfs(neighbor)
            path.pop()

        for node in graph:
            dfs(node)
        return cycles

    def topological_sort(self) -> List[str]:
        """Provides a safe topological ordering of dependencies."""
        graph = self.build_dependency_graph()
        visited = set()
        temp_mark = set()
        order = []
        
        def visit(node: str):
            if node in temp_mark:
                raise Exception(f"Not a DAG: cycle detected at {node}")
            if node not in visited:
                temp_mark.add(node)
                for neighbor in graph.get(node, []):
                    if neighbor in graph:  # Only visit known nodes
                        visit(neighbor)
                temp_mark.remove(node)
                visited.add(node)
                order.append(node)
                
        for node in sorted(graph.keys()):
            if node not in visited:
                visit(node)
                
        return order[::-1]
