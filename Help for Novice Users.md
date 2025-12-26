## How to Install Conda
Download **Anaconda** from [here](https://www.anaconda.com/download) or **Miniconda** from [here](https://docs.conda.io/en/latest/miniconda.html).

After installation, open **Anaconda Prompt** (on Windows) or Terminal (on macOS/Linux) and verify the installation:
```
conda --version
```

## How to Create a Conda Environment
Open **Anaconda Prompt** (or Terminal) and run the following commands step by step:

1. Navigate to your project folder:
```
cd path\to\your\project
```
2. Create a new environment (replace `pyhydro` with your desired name) and specify Python version:
```
conda create --name pyhydro python=3.11
```
3. Activate the environment:
```
conda activate pyhydro
```
4. Deactivate when done:
```
conda deactivate
```

## How to Install and Run Your Project
Ensure your environment is active (`conda activate pyhydro`), then install the project in editable mode:
```
pip install -e .
```

✅ **Tip:** Always use **Anaconda Prompt** and ensure your environment is active (`(pyhydro)` should appear on the left) before installing packages or running scripts. Happy coding! 🚀