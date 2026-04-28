#!/bin/bash
echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment and installing dependencies..."
source .venv/bin/activate
pip install -r requirements.txt

echo "Setup complete."
read -p "Press enter to continue"
