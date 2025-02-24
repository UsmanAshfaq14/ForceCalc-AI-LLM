import json
import csv
from typing import Dict, List, Union
from dataclasses import dataclass
import re

@dataclass
class EquationData:
    equation: str
    transformation_method: str
    variables: List[str]

class ValidationError(Exception):
    pass

class ForceCalcAI:
    VALID_TRANSFORMATION_METHODS = ["factorization", "substitution"]
    
    def __init__(self):
        self.report_sections = {
            "validation": "",
            "formulas": "",
            "transformation": "",
            "analysis": "",
            "final": ""
        }

    def validate_input(self, data: Dict) -> EquationData:
        # Check required fields
        required_fields = ["equation", "transformation_method", "variables"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValidationError(f"Missing required field(s): {', '.join(missing_fields)}")

        # Validate data types
        if not isinstance(data["equation"], str):
            raise ValidationError("Invalid data type for field: equation. Expected string.")
        if not isinstance(data["transformation_method"], str):
            raise ValidationError("Invalid data type for field: transformation_method. Expected string.")
        if not isinstance(data["variables"], list):
            raise ValidationError("Invalid data type for field: variables. Expected list.")

        # Validate transformation method
        if data["transformation_method"] not in self.VALID_TRANSFORMATION_METHODS:
            raise ValidationError("Invalid value for field: transformation_method. Please use 'factorization' or 'substitution'.")

        return EquationData(**data)

    def generate_validation_report(self, data: EquationData) -> str:
        return f"""# Data Validation Report
## 1. Data Structure Check:
- Provided Equation: {data.equation}
- Transformation Method: {data.transformation_method}
- Variables Provided: {', '.join(data.variables)}

## 2. Required Fields Check:
- equation: Present
- transformation_method: Present
- variables: Present

## 3. Data Type Validation:
- Equation (string): Valid
- Transformation Method (string, "factorization" or "substitution"): Valid
- Variables (array of strings): Valid

## Validation Summary:
Data validation is successful! Proceeding with the transformation...\n"""

    def transform_equation(self, data: EquationData) -> Dict[str, str]:
        if data.transformation_method == "factorization":
            return self._factorize_equation(data.equation, data.variables)
        else:
            return self._substitute_equation(data.equation, data.variables)

    def _factorize_equation(self, equation: str, variables: List[str]) -> Dict[str, str]:
        # Simple implementation for demonstration
        steps = []
        final_equation = equation
        
        # Find common factors
        terms = equation.split('+')
        common_vars = set.intersection(*[set(re.findall(r'[a-zA-Z]+', term)) for term in terms])
        
        if common_vars:
            common_factor = list(common_vars)[0]
            steps.append(f"Identified common factor: ${common_factor}$")
            
            # Factor out the common term
            new_terms = []
            for term in terms:
                new_term = term.replace(common_factor, '').strip('*')
                new_terms.append(new_term)
            
            final_equation = f"{common_factor}*({' + '.join(new_terms)})"
            steps.append(f"Factored equation: ${final_equation}$")
        
        return {
            "steps": steps,
            "final_equation": final_equation
        }

    def _substitute_equation(self, equation: str, variables: List[str]) -> Dict[str, str]:
        # Simple implementation for demonstration
        steps = []
        final_equation = equation
        
        # Find complex sub-expressions
        sub_expr = re.findall(r'\([^()]+\)', equation)
        if sub_expr:
            steps.append(f"Identified sub-expression: ${sub_expr[0]}$")
            steps.append(f"Substituting with X")
            
            # Perform substitution
            intermediate = equation.replace(sub_expr[0], 'X')
            steps.append(f"Intermediate equation: ${intermediate}$")
            
            # Revert substitution
            final_equation = intermediate.replace('X', sub_expr[0])
            steps.append(f"Final equation after reverting substitution: ${final_equation}$")
        
        return {
            "steps": steps,
            "final_equation": final_equation
        }

    def generate_final_report(self, data: EquationData, transformation_result: Dict[str, str]) -> str:
        formulas_section = """# Formulas and Methods Used:
1. Factorization Example:
   $$F = m \\times a + m \\times g \\quad \\Rightarrow \\quad F = m \\times (a + g)$$
2. Substitution Example:
   IF a complex sub-expression is identified (e.g., $$X = a + g$$), then substitute:
   $$F = m \\times X + c$$
   and later revert back to:
   $$X = a + g$$\n"""

        transformation_section = f"""# Equation Transformation Summary
Original Equation: ${data.equation}$
Transformation Method: {data.transformation_method}
Simplified Equation: ${transformation_result['final_equation']}$\n"""

        analysis_section = """# Detailed Analysis
## Transformation Steps:\n"""
        for i, step in enumerate(transformation_result['steps'], 1):
            analysis_section += f"Step {i}: {step}\n"

        final_section = f"""# Final Simplified Equation:
${transformation_result['final_equation']}$

# Feedback Request
Would you like detailed calculations for any specific step? Rate this analysis (1-5)."""

        return "\n".join([
            self.generate_validation_report(data),
            formulas_section,
            transformation_section,
            analysis_section,
            final_section
        ])

def process_input(input_data: Union[str, Dict]) -> str:
    calculator = ForceCalcAI()
    
    # Parse input data if it's a string
    if isinstance(input_data, str):
        try:
            if input_data.startswith('{'):
                data = json.loads(input_data)
            else:
                reader = csv.DictReader(input_data.splitlines())
                data = next(reader)
                data['variables'] = data['variables'].split(',')
        except Exception as e:
            return "ERROR: Invalid data format. Please provide data in CSV or JSON format."
    else:
        data = input_data

    try:
        # Validate input
        validated_data = calculator.validate_input(data)
        
        # Transform equation
        transformation_result = calculator.transform_equation(validated_data)
        
        # Generate final report
        return calculator.generate_final_report(validated_data, transformation_result)
        
    except ValidationError as e:
        return f"ERROR: {str(e)}"
    except Exception as e:
        return f"ERROR: An unexpected error occurred: {str(e)}"

# ... (previous code remains the same until the main section)

# Example usage
if __name__ == "__main__":
    # Example JSON input with proper structure
    example_inputs = [
    {"equation": "14m^2 + 28m", "transformation_method": "factorization", "variables": ["m"]},
    {"equation": "16n^2 + 32n", "transformation_method": "factorization", "variables": ["n"]},
    {"equation": "18*(p^2 + 5) + 9", "transformation_method": "substitution", "variables": ["p"]},
    {"equation": "20q^2 + 40q", "transformation_method": "factorization", "variables": ["q"]},
    {"equation": "22*(r^2 + 6) + 11", "transformation_method": "substitution", "variables": ["r"]},
    {"equation": "24s^2 + 48s", "transformation_method": "factorization", "variables": ["s"]},
    {"equation": "26*(t^2 + 7) + 13", "transformation_method": "substitution", "variables": ["t"]},
    {"equation": "28u^2 + 56u", "transformation_method": "factorization", "variables": ["u"]},
    {"equation": "30*(v^2 + 8) + 15", "transformation_method": "substitution", "variables": ["v"]},
    {"equation": "32w^2 + 64w", "transformation_method": "factorization", "variables": ["w"]}
    ]

    
    # Process each equation
    for i, input_data in enumerate(example_inputs, 1):
        print(f"\n{'='*50}")
        print(f"Processing Equation {i}")
        print(f"{'='*50}\n")
        print(process_input(input_data))