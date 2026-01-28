import subprocess
from pathlib import Path
import tempfile
import re


class Executor:
    """ To Execute the OpenROAD code"""
    def __init__(self,working_dir="."):
        self.working_dir=Path(working_dir)
        self.working_dir.mkdir(parents=True,exist_ok=True)

    
    def extract_code(self,text):
        pattern=r'```(?:python)?\n(.*?)\n```'
        matches=re.findall(pattern,text,re.DOTALL)
        if matches:
            return matches[0].strip()
        
        if 'from openroad import' in text or 'import openroad' in text:
            lines=text.split('\n')
            code_lines=[]
            started=False

            for line in lines:
                if 'import' in line:
                    started=True
                
                if started:
                    code_lines.append(line)

                    if line.strip() and not line.strip().startswith(('#', 'from', 'import')) and '=' not in line and '(' not in line:
                        break

            if code_lines:
                return '\n'.join(code_lines).strip()

        return None    
    
    def execute(self,code,timeout=30):
        print(f"Executing code...")
        print(f"Code preview:{code[:100]}...")

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            dir=self.working_dir,
            delete=False
        ) as f:
            f.write(code)
            temp_file=Path.f.name
        
        try:
            result=subprocess.run(
                ['python',str(temp_file)],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            temp_file.unlink()
            success=result.returncode==0
            print(f"Execution:{'Success' if success else 'Failed'}")

            return{
                'success':success,
                'stdout':result.stdout,
                'stderr':result.stderr,
                'exitcode':result.returncode
            }
        

        except subprocess.TimeoutExpired:
            if temp_file.exists():
                temp_file.unlink()
            print(f"Execution: X Timeout-{timeout}s")
            return{
                'success':False,
                'error':f'Execution timeout after {timeout}s'
            }
        
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            
            print(f"Execution: X Error-{e}")
            return {
                'success':False,
                'error':str(e)
            }
            

            