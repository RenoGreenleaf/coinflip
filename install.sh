python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
aerich init -t settings.TORTOISE
aerich init-db