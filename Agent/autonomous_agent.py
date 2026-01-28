
import torch
from transformers import AutoModelForCausalLM,AutoTokenizer
from peft import PeftModel
import json
import os

from memory_store import MemoryStore
from executor import Executor
from validator import CodeValidator
from corrector import CodeCorrector
from planner import PlannerAgent
from metrics_parser import MetricsParser
from decision_engine import DecisionEngine

class AutonomousFlowAgent:

    def __init__(self,base_model_path,adapter_path):
        self.tokenizer=AutoTokenizer.from_pretrained(
            base_model_path,
            local_files_only=False,
            use_fast=False
        )

        self.tokenizer.pad_token=self.tokenizer.eos_token
        base=AutoModelForCausalLM.from_pretrained(
            base_model_path,
            torch_dtype=torch.float16,
            local_files_only=False).to("mps" if torch.backends.mps.is_available() else "cpu")
        

        self.model=PeftModel.from_pretrained(  base, adapter_path, is_trainable=False,   local_files_only=True)
        self.model.eval()

        self.memory=MemoryStore()
        self.executor=Executor()
        self.validator=CodeValidator()
        self.corrector=CodeCorrector()
        self.planner=PlannerAgent(self.model,self.tokenizer)
        self.parser=MetricsParser()
        self.decision_engine=DecisionEngine()

    
    def run_autonomous_flow(self,user_goal,max_iterations=3,use_mock=True):

        print(f"\n{'='*70}")
        print("STARTING AUTONOMOUS FLOW")
        print(f"{'='*70}")
        print(f"Goal: {user_goal}")
        print(f"Max iterations: {max_iterations}")
        print(f"Mode: {'MOCK' if use_mock else 'REAL'}")

        iteration=0
        final_decision=None

        while iteration< max_iterations:
            iteration+=1

            print(f"\n{'='*70}")
            print(f"ITERATION {iteration}/{max_iterations}")
            print(f"{'='*70}")
            
            #Step1: Plan
            plan=self.planner.create_plan(user_goal,self.memory.state)
            self.memory.store('plan',plan)
            
            #Step2: Execute each step
            for step in plan.get('steps',[]):
                print(f"\n[Step {step['step']}] {step['description']}")
                
                code=self._generate_code(step['description'])
                is_valid,errors,warnings=self.validator.validate(code)

                if not is_valid:
                    print(f"Validation failed:{errors}")

                    code,fixes=self.corrector.auto_correct(code)
                    print(f" Applied {len(fixes)} corrections")

                if use_mock:
                    result=self.executor.mock_execute(step['action'])
                else:
                    result=self.executor.execute(code)
            
                
                self.memory.log_execution(step['step'],code,result)
                print(f"Result: {'✓' if result.get('success') else '✗'}")
            
            #Step3 : PARSE reports
            last_result=self.memory.execution_log[-1]['result']
            reports=last_result.get('reports',{})
            metrics=self.parser.parse_all(reports)
            
            #Step4 : Decide
            final_decision=self.decision_engine.evaluate(metrics)
            
            #Step5: Loop or finish
            if final_decision['status']=='success':
                print(f"\n{'='*70}")
                print("✓ GOAL ACHIEVED")
                print(f"{'='*70}")
                break

            elif iteration < max_iterations:
                print(f"\n→ Replanning to fix issues...")
            else:
                print(f"\n⚠ Max iterations reached")
        
        self.memory.save("flow_log.json")
        return {
            'goal': user_goal,
            'iterations': iteration,
            'status': final_decision['status'] if final_decision else 'incomplete',
            'total_steps':len(self.memory.execution_log)
        }
    

    def _generate_code(self,description):
        """Generate code for step description"""

        prompt=f"<s>[INST] Write OpenROAD Python code to: {description} [/INST]"
        inputs=self.tokenizer(prompt,return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs=self.model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.7,
                top_p=0.9
            )
        
        code=self.tokenizer.decode(outputs[0],skip_special_tokens=True)
        if "[/INST]" in code:
            code=code.split("[/INST]")[-1].strip()
        return code
    


if __name__ == "__main__":
    base= "mistralai/Mistral-7B-Instruct-v0.2"
    adapter = "/Users/manivannans/EDA-Corpus/openroad_mistral_7b_finetuned/checkpoint-100"
    
    agent= AutonomousFlowAgent(base,adapter)
    result= agent.run_autonomous_flow(
        user_goal="Complete RTL to GDS with timing closure",
        max_iterations=2,
        use_mock=True
    )

    print("\n" + "="*70)
    print("FINAL RESULT")
    print("="*70)
    print(json.dumps(result, indent=2))

            
    

