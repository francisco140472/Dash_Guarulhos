import os
import time
from datetime import datetime

# 🔹 Caminho do repositório LOCAL (ajuste para onde o repositório foi clonado)
REPO_PATH = r'c:\Users\franc\OneDrive\Documentos\ASSIS\vu_guarulhos_28022025\Dash_Guarulhos'

# 🔹 Configurar usuário do Git
GIT_USERNAME = "francisco140472"
GIT_EMAIL = "francisco.assis@enorsul.com.br"
GIT_BRANCH = "main"  # Verifique se é "main" ou "master"

# 🔹 Verificar se o repositório existe
if not os.path.exists(REPO_PATH):
    print(f"❌ Erro: O caminho '{REPO_PATH}' não existe.")
    exit(1)

# 🔹 Mudar para o diretório do repositório
os.chdir(REPO_PATH)

# 🔹 Função para atualizar o repositório
def atualizar_git():
    commit_message = f"Atualização automática: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    os.system(f'git config user.name "{GIT_USERNAME}"')
    os.system(f'git config user.email "{GIT_EMAIL}"')
    os.system(f'git pull origin {GIT_BRANCH}')
    os.system('git add .')
    os.system(f'git commit -m "{commit_message}"')
    os.system(f'git push origin {GIT_BRANCH}')
    
    print(f"🚀 Atualização automática concluída em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 🔹 Loop para rodar a cada 1 hora (3600 segundos)
while True:
    atualizar_git()
    print("⏳ Aguardando 1 hora para a próxima atualização...\n")
    time.sleep(3600)  # Aguarda 3600 segundos (1 hora)
