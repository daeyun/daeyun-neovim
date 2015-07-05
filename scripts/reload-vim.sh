#!/bin/sh

set -o xtrace

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

find $DIR/../rplugin/python -type f -name '*.pyc' -exec rm {} +
find $DIR/../rplugin/python -type d -name '__pycache__' -exec rm {} +

export NVIM_LISTEN_ADDRESS=/tmp/nvim2
export NVIM_PYTHON_LOG_LEVEL=DEBUG
export NVIM_PYTHON_LOG_FILE="$DIR/../logs/neovim_log.txt"
nvim -c "UpdateRemotePlugins" -c "q" && nvim $@
