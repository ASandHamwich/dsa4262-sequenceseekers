#!/bash/bin

# Update package list and install Python.
sudo apt update
sudo apt install -y python3.8 python3-pip python3.8-venv

# Verify
python3.8 --version

# Install dependencies 
pip install -r requirements.txt
