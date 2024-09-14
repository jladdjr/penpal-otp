venv:
        python3 -m venv .venv
        .venv/bin/pip3 install -r requirements-dev.txt

test:
        pytest --cov=penpal .