venv:
        #!/usr/bin/env bash
        set -x
        venv_parent_folder="$HOME/venvs"
        mkdir -p $venv_parent_folder
        rm -r ${venv_parent_folder}/penpal
        python3 -m venv ${venv_parent_folder}/penpal
        ${venv_parent_folder}/penpal/bin/pip3 install -r requirements-dev.txt

test:
        pytest --cov=penpal .

lint:
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics