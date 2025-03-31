# smart-store-houstonasherlaws
Smart Sales Starter Files
Starter files to initialize the Smart Sales project.

Project Setup Guide (Windows)
Run all commands from a PowerShell terminal in the root project folder.

Step 1 - Create a Local Project Virtual Environment
powershell
Copy
Edit
py -m venv .venv

Step 2 - Activate the Virtual Environment
powershell
Copy
Edit
.venv\Scripts\activate

Step 3 - Install Required Packages
powershell
Copy
Edit
py -m pip install --upgrade -r requirements.txt

Step 4 - (Optional) Verify Virtual Environment Setup
powershell
Copy
Edit
py -m datafun_venv_checker.venv_checker

Step 5 - Run the Initial Project Script
powershell
Copy
Edit
py scripts/data_prep.py
Initial Package List
These are the required dependencies for the project:

pip

loguru

ipykernel

jupyterlab

numpy

pandas

matplotlib

seaborn

plotly

pyspark==4.0.0.dev1

pyspark[sql]



