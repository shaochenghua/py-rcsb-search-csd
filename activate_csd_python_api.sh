source ~/CCDC/ccdc-software/csd-python-api/miniconda/bin/activate
#!/bin/bash

# Replace 'my_command' with the actual command you want to locate
CMD_PATH=$(command -v obabel)

if [ -z "$CMD_PATH" ]; then
    echo "Error: 'my_command' not found in PATH."
    exit 1
fi

# Set the environment variable
export OPENBABELCMD="$CMD_PATH"

# Optional: Print it out
echo "OPENBABELCMD set to $OPENBABELCMD"

