import os
import subprocess
import streamlit as st
import time
import threading

# Função para atualizar o código automaticamente
def atualizar_codigo():
    try:
        resultado = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
        st.sidebar.write("🔄 Verificando atualizações...")

        if "Already up to date" in resultado.stdout:
            st.sidebar.write("✅ Código já está atualizado!")
        else:
            st.sidebar.write("⚠ Atualização detectada, reiniciando o app...")
            reiniciar_app()
    except Exception as e:
        st.sidebar.write(f"❌ Erro ao atualizar: {e}")

# Função para reiniciar o app
def reiniciar_app():
    time.sleep(2)  # Pequeno delay para evitar conflitos
    os.system("streamlit run app.py")  # Substitua 'app.py' pelo nome do seu script principal
    st.sidebar.write("🔄 Reiniciando...")

# Função que verifica atualizações em segundo plano
def verificar_atualizacoes_periodicamente(intervalo=300):
    while True:
        atualizar_codigo()
        time.sleep(intervalo)  # Verifica a cada 'intervalo' segundos (ex: 300 = 5 minutos)

# Inicia a verificação automática em segundo plano
threading.Thread(target=verificar_atualizacoes_periodicamente, daemon=True).start()

# Adiciona um botão para atualização manual
if st.sidebar.button("🔄 Atualizar Agora"):
    atualizar_codigo()
