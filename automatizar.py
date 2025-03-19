import os
import subprocess
from datetime import datetime

# 🔹 Caminho do repositório LOCAL
REPO_PATH = r'c:\Users\franc\OneDrive\Documentos\ASSIS\vu_guarulhos_28022025\Dash_Guarulhos'

# 🔹 Configurar usuário do Git
GIT_USERNAME = "francisco140472"
GIT_EMAIL = "francisco.assis@enorsul.com.br"
GIT_BRANCH = "main"  # Confirme se é "main" ou "master"

# 🔹 Mensagem de commit automática
commit_message = f"Atualização automática: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# 🔹 Verificar se o repositório existe
if not os.path.exists(REPO_PATH):
    print(f"❌ Erro: O caminho '{REPO_PATH}' não existe.")
    exit(1)

# 🔹 Mudar para o diretório do repositório
os.chdir(REPO_PATH)

# 🔹 Executar comandos Git
def run_git_command(command):
    """Executa um comando Git e retorna a saída"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Erro ao executar: {command}\n{result.stderr}")
        exit(1)
    print(f"✅ {command} executado com sucesso.")

# Configurar usuário do Git
run_git_command(f'git config user.name "{GIT_USERNAME}"')
run_git_command(f'git config user.email "{GIT_EMAIL}"')

# Atualizar o repositório
run_git_command(f'git pull origin {GIT_BRANCH}')

# Adicionar arquivos ao commit
run_git_command('git add .')

# Criar commit
run_git_command(f'git commit -m "{commit_message}"')

# Enviar para o GitHub
run_git_command(f'git push origin {GIT_BRANCH}')

print("🚀 Atualização automática concluída!")
