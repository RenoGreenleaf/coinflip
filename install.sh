echo "\033[92mCreating virtual environment.\033[0m"
python -m venv .venv
source .venv/bin/activate
echo "\033[92mInstalling dependencies.\033[0m"
python -m pip install -r requirements.txt