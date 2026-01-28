#!/bin/bash
#SBATCH -p gpu
#SBATCH --gres=gpu:h200:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=8:00:00
#SBATCH --job-name=openroad_llm
#SBATCH --output=openroad_llm_%j.out
#SBATCH --error=openroad_llm_%j.err

echo "=========================================="
echo "Job started at: $(date)"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "=========================================="

############################
# 1. Load required modules
############################
module purge
module load cuda/12.1.1
module load anaconda3/2024.06

########################################
# 2. Initialize conda
########################################
source /shared/EL9/explorer/anaconda3/2024.06/etc/profile.d/conda.sh

########################################
# 3. Activate conda environment
########################################
echo "Activating conda environment: zerosim_env"
conda activate zerosim_env

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate environment zerosim_env"
    conda env list
    exit 1
fi

echo "Active environment: $CONDA_DEFAULT_ENV"

########################################
# 4. HARD BLOCK user-site Python packages
#    (THIS FIXES libcudnn.so.9 ISSUE)
########################################
export PYTHONNOUSERSITE=1
unset PYTHONPATH

########################################
# 5. Environment sanity check
########################################
echo "=========================================="
echo "Environment check"
echo "=========================================="

echo "Python executable:"
which python
python --version

echo "Torch location:"
python - << 'EOF'
import torch, sys
print("Torch file:", torch.__file__)
print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("GPU memory (GB):", round(torch.cuda.get_device_properties(0).total_memory / 1e9, 2))
    print("cuDNN enabled:", torch.backends.cudnn.enabled)
    print("cuDNN version:", torch.backends.cudnn.version())
EOF

echo "Transformers version:"
python - << 'EOF'
import transformers
print(transformers.__version__)
EOF

echo "PEFT version:"
python - << 'EOF'
import peft
print(peft.__version__)
EOF

echo "=========================================="

########################################
# 6. Offline HuggingFace configuration
########################################
export TRANSFORMERS_OFFLINE=1
export HF_DATASETS_OFFLINE=1
export HF_HOME=$HOME/.cache/huggingface
export TRANSFORMERS_CACHE=$HF_HOME/transformers
export TORCH_HOME=$HOME/.cache/torch

echo "Running in OFFLINE mode"
echo "HF cache directory: $HF_HOME"

########################################
# 7. Navigate to project directory
########################################
cd /home/senthilkumar.m/EDA-Corpus || exit 1

echo "=========================================="
echo "File checks"
echo "=========================================="

[ -f src/train.py ] || { echo "ERROR: src/train.py not found"; exit 1; }
[ -f data/train.jsonl ] || { echo "ERROR: data/train.jsonl not found"; exit 1; }
[ -f data/val.jsonl ] || { echo "ERROR: data/val.jsonl not found"; exit 1; }
[ -d cached_model ] || { echo "ERROR: cached_model/ not found"; exit 1; }

echo "✓ src/train.py found"
echo "✓ data/train.jsonl found"
echo "✓ data/val.jsonl found"
echo "✓ cached_model/ found"

echo ""
echo "Dataset size:"
wc -l data/train.jsonl data/val.jsonl
echo ""

########################################
# 8. Run training
########################################
echo "=========================================="
echo "Starting OpenROAD LLM Training"
echo "=========================================="

$CONDA_PREFIX/bin/python src/train.py

########################################
# 9. Job completion
########################################
EXIT_CODE=$?

echo ""
echo "=========================================="
echo "Job finished at: $(date)"
echo "Exit code: $EXIT_CODE"

if [ $EXIT_CODE -eq 0 ]; then
    echo "SUCCESS: Training completed"
    echo "Check model output directory as defined in train.py"
else
    echo "FAILED: Training exited with code $EXIT_CODE"
    echo "See error log: openroad_llm_${SLURM_JOB_ID}.err"
fi

echo "=========================================="
exit $EXIT_CODE
