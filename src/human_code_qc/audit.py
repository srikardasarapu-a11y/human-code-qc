import ast

class QCPipeline:
    def __init__(self):
        pass

    def run_checks(self, py_content, meta_content):
        """
        Runs static Quality Control checks.
        No code execution or LLM integration is performed here.
        Returns a dictionary of analysis results.
        """
        results = {
            "needs_repair": False,
            "issues": []
        }
        
        # 1. Metadata Checks
        validation = meta_content.get("validation", {})
        if not validation.get("syntaxValid", True):
            results["needs_repair"] = True
            results["issues"].append("Metadata reports syntax is invalid.")
            
        if not validation.get("utf8Valid", True):
            results["needs_repair"] = True
            results["issues"].append("Metadata reports UTF-8 is invalid.")

        # 2. Static Analysis: AST Parsing
        try:
            ast.parse(py_content)
        except SyntaxError as e:
            results["needs_repair"] = True
            results["issues"].append(f"AST Parsing failed: {e}")
            
        return results
