#!/bin/bash
# Usage: ./submit.sh <python_script.py>
# Submits a Python script to the PBS queue

if [ $# -eq 0 ]; then
    echo "Usage: ./submit.sh <python_script.py>"
    echo "Example: ./submit.sh test.py"
    exit 1
fi

SCRIPT_PATH="$1"

# Check if file exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: File '$SCRIPT_PATH' not found"
    exit 1
fi

# Check if it's a Python file
if [[ ! "$SCRIPT_PATH" == *.py ]]; then
    echo "Warning: File does not have .py extension"
fi

# Get absolute path
FULL_PATH=$(realpath "$SCRIPT_PATH")

# Submit the job with the Python script as a variable
echo "Submitting job for: $FULL_PATH"
qsub -v PYTHON_SCRIPT="$FULL_PATH" submit.pbs

echo "Job submitted successfully!"
