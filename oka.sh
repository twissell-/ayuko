#!/bin/bash -eu

OKA_PATH="$(dirname "${BASH_SOURCE[0]}")"

function create_virtualenv() {
    echo "Creating virtualenv"
    virtualenv "${OKA_PATH}/venv" -p python3
    "${OKA_PATH}/venv/bin/pip" install -r requirements.txt
}

if [[ ! -f "${OKA_PATH}/venv/bin/python" ]]; then
    create_virtualenv
fi

"${OKA_PATH}/venv/bin/python" "${OKA_PATH}/cli.py" "$@"
