import subprocess

try:
    subprocess.run(["python", "-m", "streamlit", "run", "test_jortform.py", "--server.port", "8501", "--server.headless", "true"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Erro ao rodar o Streamlit: {e}")
