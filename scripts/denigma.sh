#!/bin/bash

# Function to determine Python command
get_python_cmd() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    elif command -v py &> /dev/null; then
        echo "py"
    else
        echo "Python not found!" >&2
        exit 1
    fi
}

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Use python to run main.py
PYTHON_CMD=$(get_python_cmd)
if [ $? -eq 0 ]; then
    # if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    #     # Windows - use py launcher
    #     py "${SCRIPT_DIR}/main.py" "$@"
    # else
        # Linux/Unix
    $PYTHON_CMD "${SCRIPT_DIR}/../main.py" "$@"
    # fi
fi