from typing import List, Dict, Any

class DependencyGraph:
    """Sorts methodologies based on dependency requirements."""
    
    @staticmethod
    def topological_sort(plugin_ids: List[str], registry_caps: Dict[str, Any]) -> List[str]:
        """
        Sorts the plugin_ids so that dependencies are executed before the plugins that depend on them.
        """
        in_degree = {pid: 0 for pid in plugin_ids}
        adj_list = {pid: [] for pid in plugin_ids}
        
        # Build graph
        for pid in plugin_ids:
            cap = registry_caps.get(pid, {})
            deps = cap.get("dependencies", [])
            for dep in deps:
                if dep in plugin_ids:
                    adj_list[dep].append(pid)
                    in_degree[pid] += 1
                    
        # Sort
        queue = [pid for pid in plugin_ids if in_degree[pid] == 0]
        sorted_order = []
        
        while queue:
            node = queue.pop(0)
            sorted_order.append(node)
            for neighbor in adj_list[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if len(sorted_order) != len(plugin_ids):
            raise ValueError("Circular dependency detected in Platform 10 capabilities.")
            
        return sorted_order
