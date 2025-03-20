import os
import time
from datetime import datetime

REPO_DIR = r"C:\Users\franc\OneDrive\Documentos\GitHub\Dash_Guarulhos"

while True:
    try:
        os.chdir(REPO_DIR)
        os.system('git add .')
        os.system(f'git commit -m "Atualização automática: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"')
        os.system('git pull origin main --rebase')  # Evita conflitos
        os.system('git push origin main')

        print(f"✅ Atualização enviada para o GitHub em {datetime.now()}")

    except Exception as e:
        print(f"❌ Erro ao atualizar: {e}")

    print("⏳ Aguardando 1 hora para a próxima atualização...\n")
    time.sleep(10)  # Espera 1 hora antes de rodar novamente
