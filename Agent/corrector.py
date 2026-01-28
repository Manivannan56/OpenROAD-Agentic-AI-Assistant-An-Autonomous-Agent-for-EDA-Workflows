class CodeCorrector:
    def __init__(self):
        self.corrections={
            # Method name fixes
            'parseVerilogFile':'readVerilog',
            'loadVerilog':'readVerilog',
            'design.linK_design':'design.link',
            'design.compile':'# Remove - not OpenROAD API ',
            
            # Non-existent APIs
            'ord.Flow()':'# Use individual commands',
            'runRTL2PDN':'# Use step-by-step commands',
            'design.synthesize': '#Synthesis done seperately',
            
            # Parameter name fixes
            'density=':'utilization=',
            'aspect_ratio=':'aspect_ratio=',
        }
    
    def auto_correct(self,code):
        corrected=code
        fixes=[]

        for wrong,right in self.corrections:
            if wrong in corrected:
                corrected=corrected.replace(wrong,right)
                fixes.append(f"{wrong}->{right}")

        return corrected,fixes
    

    def clean_code(self,code):
        lines=code.split('\n')
        cleaned=[]

        for line in lines:
            if line.strip() in ['#','# Remove']:
                continue
            cleaned.append(line)
        
        return '\n'.join(cleaned)
    
