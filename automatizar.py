import os
import subprocess
import time
from datetime import datetime

# Configuração do usuário do Git
GIT_USER = "francisco140472"
GIT_EMAIL = "francisco.assis@enorsul.com.br"
REPO_DIR = r"C:\Users\franc\OneDrive\Documentos\GitHub\Dash_Guarulhos"  # Caminho do repositório
INTERVALO = 3600  # Intervalo de tempo (1 hora = 3600 segundos)

def run_git_command(command):
    """Executa um comando Git e retorna True se bem-sucedido, False caso contrário."""
    try:
        result = subprocess.run(command, shell=True, cwd=REPO_DIR, text=True, capture_output=True)
        if result.returncode == 0:
            print(f"✅ {command} executado com sucesso.")
            return True
        else:
            print(f"❌ Erro ao executar: {command}\n{result.stderr}")
            return False
    except Exception as e:
        print(f"⚠ Erro inesperado: {e}")
        return False

# Configurar usuário do Git (caso necessário)
run_git_command(f'git config user.name "{GIT_USER}"')
run_git_command(f'git config user.email "{GIT_EMAIL}"')

while True:
    print("\n🔄 Iniciando atualização automática...\n")

    # Atualizar o repositório antes de fazer modificações
    run_git_command("git pull origin main --rebase")

    # Verificar se há mudanças antes de tentar um commit
    status_result = subprocess.run("git status --porcelain", shell=True, cwd=REPO_DIR, text=True, capture_output=True)
    if status_result.stdout.strip():  # Se houver mudanças
        run_git_command("git add .")

        # Criar mensagem de commit com data/hora
        commit_message = f"Atualização automática: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if run_git_command(f'git commit -m "{commit_message}"'):
            run_git_command("git push origin main")
    else:
        print("⚠ Nenhuma alteração detectada. Nada para commit.")

    print(f"\n⏳ Aguardando {INTERVALO // 60} minutos para a próxima atualização...\n")
    time.sleep(INTERVALO)  # Aguarda 1 hora antes de repetir
