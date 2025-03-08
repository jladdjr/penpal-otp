venv:
        #!/usr/bin/env bash
        set -x
        venv_parent_folder="$HOME/venvs"
        mkdir -p $venv_parent_folder
        rm -r ${venv_parent_folder}/noirnet
        python3 -m venv ${venv_parent_folder}/noirnet
        ${venv_parent_folder}/noirnet/bin/pip3 install -r requirements-dev.txt
        ${venv_parent_folder}/noirnet/bin/pip3 install -e .

test_with_pdb:
        #!/usr/bin/env bash
        venv_parent_folder="$HOME/venvs"
        ${venv_parent_folder}/noirnet/bin/pytest --pdb --cov=noirnet --cov-fail-under=70

test:
        #!/usr/bin/env bash
        venv_parent_folder="$HOME/venvs"
        ${venv_parent_folder}/noirnet/bin/pytest --cov=noirnet --cov-fail-under=50

lint:
        #!/usr/bin/env bash
        venv_parent_folder="$HOME/venvs"
        ${venv_parent_folder}/noirnet/bin/black .