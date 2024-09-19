venv:
        python3 -m venv .venv
        .venv/bin/pip3 install -r requirements-dev.txt

test:
        pytest --cov=penpal .

lint:
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics