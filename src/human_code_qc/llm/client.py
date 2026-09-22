from ..config import LITELLM_BASE_URL, LITELLM_MODEL, LITELLM_MASTER_KEY

# Configure LiteLLM globally
def _configure_litellm():
    import litellm
    litellm.api_base = LITELLM_BASE_URL
    litellm.api_key = LITELLM_MASTER_KEY
    return litellm


MASTER_BUILD_PROMPT = """You are an expert software engineer and Python competitive programmer.
Your task is to repair the provided Python code so that it successfully solves the given problem statement without any syntax or logic errors.

Rules:
1. ONLY return the valid Python code.
2. Do not include markdown formatting (e.g. ```python) in your response, just the raw code.
3. Do not include any explanations or comments unless they were part of the original code.
4. Make sure the code strictly conforms to the input/output constraints mentioned in the problem metadata.
5. Fix the specific issues identified in the quality control step.
"""

class LLMRepairEngine:
    def __init__(self, enable_repair=False):
        self.enable_repair = enable_repair

    def attempt_repair(self, py_content, meta_content, issues):
        """
        Attempts to repair the given python code based on the issues found.
        """
        if not self.enable_repair:
            return py_content, False

        try:
            problem_context = meta_content.get("problem", {})
            title = problem_context.get("title", "Unknown")
            statement = problem_context.get("problemStatement", "")
            
            issues_text = "\n".join([f"- {issue}" for issue in issues])
            
            user_prompt = f"Problem: {title}\nDescription: {statement}\n\nThe following code has these issues:\n{issues_text}\n\nCode:\n{py_content}\n\nPlease provide the repaired code."

            litellm = _configure_litellm()
            response = litellm.completion(
                model=LITELLM_MODEL,
                messages=[
                    {"role": "system", "content": MASTER_BUILD_PROMPT},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            repaired_code = response.choices[0].message.content.strip()
            
            if repaired_code.startswith("```python"):
                repaired_code = repaired_code[9:]
            if repaired_code.startswith("```"):
                repaired_code = repaired_code[3:]
            if repaired_code.endswith("```"):
                repaired_code = repaired_code[:-3]
                
            return repaired_code.strip(), True
            
        except Exception as e:
            print(f"Error during LLM repair: {e}")
            return py_content, False
