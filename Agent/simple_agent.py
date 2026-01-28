import torch
import os
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


class SimpleAgent:
    def __init__(self,base_model_path,adaptor_path):
       
        self.tokenizer=AutoTokenizer.from_pretrained(
            base_model_path,
            use_fast=False,
            local_files_only=False
        )
        self.tokenizer.pad_token=self.tokenizer.eos_token

        self.base_model=AutoModelForCausalLM.from_pretrained(
            base_model_path,
            torch_dtype=torch.float16,
            local_files_only=False
        ).to("mps" if torch.backends.mps.is_available() else "cpu")

        self.model=peft.PeftModel.from_pretrained(
            self.base_model,
            adaptor_path,
            is_trainable=False
        )
        self.model.eval()
    
    def ask(self,question,max_length=256):
        prompt=f"""<s>[INST] You are an openroad expert openroad assistant. {question}[/INST]"""
        inputs=self.tokenizer(prompt,return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs=self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response=self.tokenizer.decode(outputs[0],skip_special_tokens=True)
        
        if "[/INST]" in response:
            response=response.strip("[/INST]")[-1].strip()
        
        return response
    

    def interactive_mode(self):
        print("\n" + "="*70)
        print("Interactive Mode - Type 'quit' to exit")
        print("="*70 + "\n")

        while True:
            try:
                question=input("You: ").strip()
                
                if not question:
                    continue
                if question.lower() in ['quit','exit','q']:
                    print("/Goodbye")
                    break
                print("\nAgent",end="",flush=True)
                answer=self.ask(question)
                print(answer+"\n")

            except KeyboardInterrupt:
                print("\nGoodbye")
                break

if __name__=="__main__":

    BASE="mistralai/Mistral-7B-Instruct-v0.2"
    ADAPTER = "./models/openroad_mistral_7b_finetuned"

 
    agent=SimpleAgent(BASE,ADAPTER)

    questions=["What is floorplanning in OpenROAD?", "Write Python code to read a Verilog file"]
   
    for question in questions:
        print(agent.ask(question))

    agent.interactive_mode()
    







    
        



        







