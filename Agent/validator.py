import re

class CodeValidator:

    def __init__(self):
        self.valid_imports=[
            'from openroad import',
            'import openroad',
            'import odb' 
        ]

        self.valid_methods=[
            'readVerilog',
            'readDef',
            'readLef',
            'readLib',
            'link',
            'initialize_floorplan',
            'global_placement',
            'detailed_placement',
            'clock_tree_synthesis',
            'global_route',
            'detailed_route'
        ]

        self.invalid_patterns=[
            'parseVerilogFile',
            'ord.Flow()',
            'runRTL2PDN',
            'design.compile()',
        ]
    
    def validate(self,code):
        errors=[]
        warnings=[]

        has_import=any(imp in code for imp in self.valid_imports)
        if not has_import:
            errors.append("Missing OpenROAD imports")
        
        try:
            compile(code,'<string>','exec')
        except SyntaxError as e:
            errors.append(f"Syntax error:{e}")
        
        for invalid in self.invalid_patterns:
            if invalid in code:
                errors.append(f"Invalid API call: {invalid}")

        if len(code)<20:
            warnings.append("Code seems to be short")
        if len(code)>2000:
            warnings.append("Code seems very long")

    def get_suggestions(self,errors):

        suggestions=[]
        for error in errors:
            if 'parseVerilogFile' in error:
                suggestions.append("Use design.readVerilog() instead") 
            elif 'Flow()' in error:
                suggestions.append("Use individual OpenROAD commands")
            elif  'Missing OpenROAD imports' in error:
                suggestions.append("Add: from openroad import Tech, Design")  

        return suggestions
   