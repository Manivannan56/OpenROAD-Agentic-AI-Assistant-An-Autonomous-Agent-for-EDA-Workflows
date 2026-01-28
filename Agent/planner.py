#!/usr/bin/env python3
"""
planner.py
Planner Agent - Creates execution plans using LLM
"""
import torch
import json
import re


class PlannerAgent:
    """Creates multi-step execution plans"""
    
    def __init__(self, model, tokenizer):
        """
        Initialize planner.
        
        Args:
            model: LLM model
            tokenizer: Tokenizer
        """
        self.model = model
        self.tokenizer = tokenizer
    
    def create_plan(self, user_goal, current_state=None):
        """
        Create execution plan for goal.
        
        Args:
            user_goal: High-level user goal
            current_state: Optional current state
            
        Returns:
            dict: JSON plan with steps
        """
        print(f"\n{'='*70}")
        print("PLANNER: Creating execution plan")
        print(f"{'='*70}")
        
        # Build prompt
        state_info = ""
        if current_state:
            state_info = f"\n\nCurrent state: {json.dumps(current_state, indent=2)}"
        
        prompt = f"""<s>[INST] You are an OpenROAD execution planner. Create a JSON plan.

        Goal: {user_goal}{state_info}

        Output ONLY valid JSON:
        {{
        "goal": "{user_goal}",
        "steps": [
            {{"step": 1, "action": "read_design", "description": "Read Verilog and tech files"}},
            {{"step": 2, "action": "floorplan", "description": "Initialize floorplan"}},
            ...
        ]
        }}
        [/INST]"""
        
        # Generate
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.3,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if "[/INST]" in response:
            response = response.split("[/INST]")[-1].strip()
        
        # Parse JSON
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
                print(f"Plan created: {len(plan.get('steps', []))} steps")
                return plan
        except Exception as e:
            print(f"JSON parse failed: {e}")
        
        # Fallback
        print("Using default plan")
        return self._default_rtl_to_gds_plan()
    
    def _default_rtl_to_gds_plan(self):
        """Default RTL→GDS plan"""
        return {
            "goal": "RTL to GDS",
            "steps": [
                {"step": 1, "action": "read_design", "description": "Read Verilog, LEF, LIB files"},
                {"step": 2, "action": "floorplan", "description": "Initialize floorplan with 70% utilization"},
                {"step": 3, "action": "placement", "description": "Global and detailed placement"},
                {"step": 4, "action": "cts", "description": "Clock tree synthesis"},
                {"step": 5, "action": "routing", "description": "Global and detailed routing"},
                {"step": 6, "action": "write_gds", "description": "Write GDS output"}
            ]
        }


