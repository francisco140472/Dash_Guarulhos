import os
import sys
import time
from datetime import datetime

# 🔹 Configurar UTF-8 para evitar erros com emojis no terminal
sys.stdout.reconfigure(encoding='utf-8')

# 🔹 Caminho do repositório LOCAL (ajuste para onde seu repositório foi clonado)
REPO_PATH = r'c:\Users\franc\OneDrive\Documentos\GitHub\Dash_Guarulhos'

# 🔹 Configurar usuário do Git
GIT_USERNAME = "francisco140472"
GIT_EMAIL = "francisco.assis@enorsul.com.br"
GIT_BRANCH = "main"  # Verifique se é "main" ou "master"

# 🔹 Intervalo de atualização (em segundos) → Exemplo: 1 hora = 3600 segundos
INTERVALO_ATUALIZACAO = 3600  # Altere para o tempo desejado

def rodar_comando(comando):
    """Executa um comando do sistema e exibe a saída"""
    resultado = os.popen(comando).read()
    print(resultado)
    return resultado

def atualizar_git():
    """Atualiza o repositório no GitHub automaticamente"""
    print("\n🔄 Iniciando atualização automática...\n")

    # 🔹 Verificar se o repositório existe
    if not os.path.exists(REPO_PATH):
        print(f"❌ Erro: O caminho '{REPO_PATH}' não existe.")
        return

    # 🔹 Mudar para o diretório do repositório
    os.chdir(REPO_PATH)

    # 🔹 Configurar usuário do Git
    rodar_comando(f'git config user.name "{GIT_USERNAME}"')
    rodar_comando(f'git config user.email "{GIT_EMAIL}"')

    # 🔹 Puxar as últimas atualizações do repositório remoto
    rodar_comando(f'git pull origin {GIT_BRANCH}')

    # 🔹 Adicionar arquivos novos/modificados ao commit
    rodar_comando('git add .')

    # 🔹 Criar commit com mensagem automática
    commit_message = f"Atualização automática: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    rodar_comando(f'git commit -m "{commit_message}"')

    # 🔹 Enviar as alterações para o GitHub
    rodar_comando(f'git push origin {GIT_BRANCH}')

    print(f"🚀 Atualização automática concluída em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 🔄 Loop para atualizar automaticamente a cada X horas
while True:
    atualizar_git()
    print(f"⏳ Aguardando {INTERVALO_ATUALIZACAO / 3600:.1f} hora(s) para a próxima atualização...\n")
    time.sleep(INTERVALO_ATUALIZACAO)
