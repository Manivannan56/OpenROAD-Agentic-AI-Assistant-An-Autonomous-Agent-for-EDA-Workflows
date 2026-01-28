# 🔧 OpenROAD Agentic AI Assistant: An Autonomous Agent for EDA Workflows

> An agentic AI assistant with fine-tuned Mistral-7B model trained on the [EDA Corpus](https://github.com/facebookresearch/EDA-Corpus) for OpenROAD workflows - providing code assistance, explanations, and workflow guidance for electronic design automation tasks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenROAD](https://img.shields.io/badge/OpenROAD-Specialized-green.svg)](https://theopenroadproject.org/)
[![Training Data: EDA Corpus](https://img.shields.io/badge/Training-EDA%20Corpus-blue)](https://github.com/facebookresearch/EDA-Corpus)

---

<p align="center">
  <img src="assets/sample_output.png" alt="Verilog Reading Comparison" width="90%">
</p>


##  What This Project Is

An **autonomous agent system** that assists with OpenROAD EDA workflows through:

**Intelligent Planning** - Breaks down high-level goals into executable steps  
**Code Generation** - Produces Python/TCL snippets for OpenROAD tasks  
 **Self-Validation** - Checks code quality before execution  
 **Auto-Correction** - Fixes common mistakes automatically  
 **Workflow Guidance** - Explains RTL-to-GDS flow and best practices  

**Architecture:** Single LLM-powered agent with structured workflow components (Planner → Generator → Validator → Corrector → Executor → Decision Engine)

---

## 🎓 Training Data: EDA Corpus v1

This model was fine-tuned on the **[EDA Corpus v1](https://github.com/facebookresearch/EDA-Corpus)**, a curated dataset specifically for OpenROAD:

- **Total Training Examples:** 1,533 data pairs (augmented)
  - Question-Answer pairs: 590 (OpenROAD concepts, tools, workflows)
  - Prompt-Script pairs: 943 (Python API examples for OpenROAD)
  
- **Data Sources:**
  - OpenROAD GitHub issues and discussions
  - Official OpenROAD documentation
  - OpenROAD-flow-scripts examples
  
- **Focus:** Python API for OpenROAD (leverages pretrained LLM Python knowledge)

### Why Python API Training Matters

The EDA Corpus focuses on Python examples rather than TCL because:
- Python code examples are more prevalent in pretraining data
- Easier to leverage existing LLM Python capabilities
- OpenROAD provides both Python and TCL interfaces

**Note:** This explains why the model generates Python API calls - the training data is Python-focused, though OpenROAD is traditionally TCL-based.

---

##  Current Capabilities & Limitations

### What Works Well (60-80% Quality)

 **Explaining OpenROAD Concepts**
- Understanding of RTL-to-GDS flow
- Tool-specific knowledge (DFSPlacer, OCts, OpenSTA)
- File format requirements (.def, .lef, .lib)

**Python API Code Assistance**
- Correct import statements (`from openroad import Tech, Design`)
- Basic API structure and patterns
- Simple task snippets

**Workflow Planning**
- Breaking down complex goals into steps
- Sequencing operations correctly
- Understanding dependencies

### Current Limitations (60-70% Quality)

 **Complex Script Generation**
- Multi-step TCL scripts have accuracy issues
- Command parameters may need verification
- Some hallucinated commands (training data artifact)

 **TCL vs Python Mix**
- Model trained primarily on Python examples
- TCL generation less reliable than Python
- May mix Python patterns into TCL code

 **Full Automation**
- Cannot reliably execute complete RTL-to-GDS flows without supervision
- Requires human validation for production use
- Template-based approach recommended for critical paths

---

##  Ongoing Development

### Active Improvements

1. **Enhanced Training Data**
   - Web scraping validated OpenROAD examples
   - Curating pure TCL scripts (not mixed with Python)
   - Filtering out hallucinated commands from training

2. **Hybrid Approach**
   - Template library for common operations (100% accuracy)
   - LLM for adaptations and variations
   - Validation pipeline against real OpenROAD

3. **Better Validation**
   - Semantic API checking (not just syntax)
   - Testing against OpenROAD documentation
   - Command existence verification

**Target:** 80%+ code quality for production use by Q2 2026

---

##  Example: Domain Knowledge vs Generic LLMs

### Reading Verilog Files

<table>
<tr>
<th width="50%"> Base Mistral-7B (Generic)</th>
<th width="50%"> EDA Corpus Fine-tuned</th>
</tr>
<tr>
<td>

```python
# Hallucinates wrong libraries
from pynq import Verilator, FPGA
v = Verilator(verilog_file)
v.compile()
```

**Problem:** `pynq` is for FPGAs, `Verilator` is a simulator - neither are OpenROAD!

</td>
<td>

```python
# Uses actual OpenROAD API
from openroad import Tech, Design
tech = Tech()
design = Design(tech)
design.readVerilog("design.v")
design.link("top")
```

**Correct:** Actual OpenROAD Python imports and API structure

</td>
</tr>
</table>

**Impact:** Saves hours debugging non-existent APIs

---

## 📊 Performance Evaluation

Evaluated on 8 OpenROAD knowledge and code generation tasks:

| Category | Base Mistral | Fine-tuned | Improvement |
|----------|-------------|-----------|-------------|
| **Concept Explanation** | 40/100 | 75/100 | +87%  |
| **Python API Knowledge** | 30/100 | 70/100 | +133%  |
| **Workflow Guidance** | 35/100 | 72/100 | +106% |
| **Simple Code Snippets** | 35/100 | 65/100 | +86%  |
| **Complex TCL Scripts** | 30/100 | 40/100 | +33%  |

**Overall:** Base 40/100 → Fine-tuned 64/100 (+60% improvement)

*Detailed evaluation: [evaluation/comparison_results.json](evaluation/comparison_results.json)*

---

##  Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/openroad-ai-assistant.git
cd openroad-ai-assistant

# Install dependencies
pip install -r requirements.txt

# Download model and adapter
# [Instructions for downloading fine-tuned weights]
```

### Basic Usage - Simple Code Generation

```python
from simple_agent import SimpleAgent

# Initialize agent
agent = SimpleAgent(
    base_model="mistralai/Mistral-7B-Instruct-v0.2",
    adapter_path="./models/openroad_finetuned"
)

# Get code snippet
response = agent.ask("How do I read a Verilog file in OpenROAD?")
print(response)
```

### Autonomous Flow Agent

```python
from autonomous_agent import AutonomousFlowAgent

# Initialize autonomous agent
agent = AutonomousFlowAgent(
    base_model="mistralai/Mistral-7B-Instruct-v0.2",
    adapter_path="./models/openroad_finetuned"
)

# Run in mock mode (for testing)
result = agent.run_autonomous_flow(
    user_goal="Create floorplan with 70% utilization",
    max_iterations=2,
    use_mock=True  # Set False for real OpenROAD execution
)

print(f"Status: {result['status']}")
print(f"Steps completed: {result['total_steps']}")
```

### Testing the Agent

```bash
# Run comprehensive component tests
python test_autonomous_agent.py --full --verbose

# Test specific components
python test_autonomous_agent.py --component planner
python test_autonomous_agent.py --component validator

# Generate test report
python test_autonomous_agent.py --full -o my_test_report.json
```

---

## 🏗️ Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  AUTONOMOUS AGENT                        │
│                                                          │
│  User Goal → Planner → Generator → Validator            │
│                 ↓          ↓           ↓                 │
│              Memory ← Corrector ← Decision Engine        │
│                 ↓          ↓           ↓                 │
│              Executor → Metrics → Next Iteration         │
└─────────────────────────────────────────────────────────┘
```

**Note:** This is a **single agent with structured workflow**, not a multi-agent system. All components share one LLM instance.

### Components

- **Planner Agent:** Creates execution plans using fine-tuned LLM
- **Code Generator:** Produces OpenROAD Python/TCL code
- **Validator:** Checks syntax and basic API correctness
- **Corrector:** Auto-fixes common patterns (limited to ~4 rules)
- **Executor:** Runs code (mock mode for testing, real mode requires OpenROAD)
- **Decision Engine:** Evaluates results and decides next steps
- **Memory Store:** Maintains conversation and execution history
- **Metrics Parser:** Extracts timing/area/power metrics from reports

---

##  Use Cases

###  Recommended Uses

1. **Learning OpenROAD**
   - Understanding concepts and workflows
   - Exploring API structure
   - Getting started with examples

2. **Code Assistance**
   - Quick snippets for common tasks
   - API reference lookup
   - Prototyping ideas

3. **Documentation Supplement**
   - Alternative explanations of concepts
   - Workflow visualization
   - Quick reference

4. **Educational Projects**
   - Teaching EDA flows
   - Research prototypes
   - Algorithm exploration

###  Not Recommended For

1.  **Production Chip Tapeouts** - Without extensive human review
2.  **Critical Path Automation** - Validation required
3.  **Safety-Critical Designs** - Human oversight mandatory
4.  **Replacing Verified Scripts** - Use as reference, not replacement

**Always validate generated code** against OpenROAD documentation and test thoroughly.

---

##  Training Details

### Model Architecture
- **Base Model:** Mistral-7B-Instruct-v0.2 (7 billion parameters)
- **Fine-tuning Method:** LoRA (Low-Rank Adaptation)
  - Rank: 16
  - Alpha: 32
  - Target modules: q_proj, v_proj
- **Training Framework:** Hugging Face PEFT

### Training Data Statistics
- **Dataset:** EDA Corpus v1 (augmented)
- **Total Examples:** 1,533
  - Question-Answer: 590 pairs
  - Prompt-Script: 943 pairs
- **Augmentation:**
  - Paraphrased prompts for diversity
  - Parameter variations
  - Variable name changes

### Data Composition
- **OpenROAD General:** Concepts, terminology, background
- **OpenROAD Tools:** DFSPlacer, OCts, OpenSTA, TritonRoute
- **OpenROAD Flow:** RTL-to-GDS workflow steps
- **Python API:** Database manipulation, design operations
- **File Formats:** .def, .lef, .lib, .sdc

### Training Configuration
- **Hardware:** [Your GPU configuration]
- **Training Time:** [X hours]
- **Learning Rate:** 2e-4
- **Batch Size:** 4
- **Epochs:** 3

---

##  Testing & Validation

### Comprehensive Test Suite

```bash
# Full test suite (all components + integration)
python test_autonomous_agent.py --full --verbose

# Individual component tests
python test_autonomous_agent.py --component memory_store
python test_autonomous_agent.py --component executor
python test_autonomous_agent.py --component validator

# Code generation quality test
python compare_base_vs_finetuned.py

# Integration tests only
python test_autonomous_agent.py --integration
```

### Test Coverage
-  Component unit tests (7 components)
-  Integration tests (component interactions)
-  End-to-end flow tests (mock mode)
-  Error handling tests
-  Code quality evaluation
-  Real OpenROAD execution (requires installation)

---

##  Repository Structure

```
openroad-ai-assistant/
├── Agents/
│   ├── autonomous_agent.py     # Main autonomous agent
│   ├── simple_agent.py         # Simple Q&A agent
│   ├── planner.py              # Planning component
│   ├── executor.py             # Code execution
│   ├── validator.py            # Code validation
│   ├── corrector.py            # Auto-correction
│   ├── decision_engine.py      # Decision making
│   ├── memory_store.py         # State management
│   └── metrics_parser.py       # Metrics extraction
├── models/
│   └── openroad_finetuned/     # Fine-tuned adapter weights
├── examples/
│   ├── explanations/           # Concept explanations
│   ├── code_snippets/          # Code examples
│   └── comparisons/            # Base vs Fine-tuned
├── evaluation/
│   ├── test_prompts.txt        # Evaluation prompts
│   ├── results.json            # Comparison results
│   └── analysis.md             # Performance analysis
├── test_autonomous_agent.py    # Comprehensive test suite
├── compare_base_vs_finetuned.py # Model comparison
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── LICENSE                     # MIT License
```

---

##  Contributing

We welcome contributions! Areas where help is needed:

1. **Training Data Curation**
   - Collecting validated OpenROAD TCL examples
   - Filtering hallucinated commands
   - Adding diverse workflow examples

2. **Validation Tools**
   - Testing against real OpenROAD
   - API correctness checking
   - Semantic validation

3. **Template Library**
   - Pre-validated TCL templates
   - Common workflow patterns
   - Error handling examples

4. **Testing & Documentation**
   - Expanding test coverage
   - Improving examples
   - Tutorial creation

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📊 Roadmap

### Current (v0.1) - Educational Assistant
-  Concept explanations
-  Python API code assistance
-  Workflow guidance
-  Basic autonomous planning
-  Limited complex automation

### Next (v0.2) - Hybrid Approach
-  Template library for critical operations
-  Clean TCL-only training data
-  Real OpenROAD validation pipeline
-  Improved error detection
-  Better TCL generation

### Future (v1.0) - Production-Ready
-  80%+ code generation accuracy
-  Full RTL-to-GDS automation support
-  Real-time OpenROAD integration
-  Multi-design optimization
-  Community template library

---

## 📖 Related Work & Citations

### This Work

If you use this project in research, please cite:

```bibtex
@software{openroad_ai_assistant_2026,
  author = {Kumar, Senthil M.},
  title = {OpenROAD AI Assistant: An Autonomous Agent for EDA Workflows},
  year = {2026},
  institution = {Northeastern University},
  url = {https://github.com/yourusername/openroad-ai-assistant}
}
```

### EDA Corpus (Training Data)

This work was trained on the EDA Corpus. Please also cite:

```bibtex
@inproceedings{wu2024eda,
  title        = {EDA Corpus: A Large Language Model Dataset for Enhanced Interaction with OpenROAD},
  author       = {Wu, Bing-Yue and Sharma, Utsav and Kankipati, Sai Rahul Dhanvi and Yadav, Ajay and George, Bintu Kappil and Guntupalli, Sai Ritish and Rovinski, Austin and Chhabria, Vidya A.},
  booktitle    = {The First IEEE International Workshop on LLM-Aided Design (LAD'24)},
  month        = {June},
  year         = {2024},
  organization = {IEEE},
  address      = {New York, NY}
}
```

---

## ⚖️ License

This project: **MIT License** - See [LICENSE](LICENSE)

Training data (EDA Corpus): **CC BY 4.0** - See [EDA Corpus License](https://github.com/facebookresearch/EDA-Corpus#license)

---

##  Acknowledgments

- **[EDA Corpus](https://github.com/facebookresearch/EDA-Corpus)** - Training dataset (Wu et al., 2024)
- **[OpenROAD Project](https://theopenroadproject.org/)** - Open-source EDA tools
- **[Mistral AI](https://mistral.ai/)** - Base language model
- **[Hugging Face](https://huggingface.co/)** - Training infrastructure & PEFT
- **Northeastern University** - Research support

---

##  Contact & Support

- **Author:** Senthil Kumar M.
- **Institution:** Northeastern University
- **Email:** [kumar.se@northeastern.edu]
- **Issues:** [GitHub Issues](https://github.com/yourusername/openroad-ai-assistant/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/openroad-ai-assistant/discussions)

---

##  Disclaimer

This is a research prototype and educational tool. Generated code should be:
-  Reviewed by humans before use
-  Tested in your specific environment
-  Validated against OpenROAD documentation
-  Version-controlled
-  Backed up before automation

**The authors are not responsible for issues arising from use of generated code in production environments.**

---

##  Keywords

Electronic Design Automation, EDA, OpenROAD, RTL-to-GDS, Physical Design, Large Language Models, LLM, Code Generation, Autonomous Agents, LoRA Fine-tuning, Mistral, VLSI, Chip Design

---

**Project Status:** Active Development |  Educational Tool |  Code Assistant  
**Goal:** Production-ready automation with human-in-the-loop validation