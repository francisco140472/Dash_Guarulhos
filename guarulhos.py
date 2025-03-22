import os
import subprocess
import streamlit as st
import time

# Criando uma variável de estado para indicar se há uma atualização pendente
if "atualizacao_pendente" not in st.session_state:
    st.session_state.atualizacao_pendente = False

# Função para atualizar o código automaticamente
def atualizar_codigo():
    try:
        resultado = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
        st.sidebar.markdown("🔄 Verificando atualizações...")

        if "Already up to date" in resultado.stdout:
            st.sidebar.markdown("✅ Código já está atualizado!")
        else:
            st.sidebar.markdown("⚠ Atualização detectada, reiniciando o app...")
            st.session_state.atualizacao_pendente = True  # Marca que precisa reiniciar
    except Exception as e:
        st.sidebar.markdown(f"❌ Erro ao atualizar: {e}")

# Função para reiniciar o app
def reiniciar_test_jortform():
    st.sidebar.markdown("🔄 Reiniciando...")
    time.sleep(2)
    os.system("streamlit run test_jortform.py")  # Substitua pelo nome correto do script principal

# Interface no Streamlit
st.sidebar.title("Gerenciamento do App")

# Botão para atualização manual (com key única)
if st.sidebar.button("🔄 Atualizar Agora", key="atualizar_btn"):
    atualizar_codigo()

# Se uma atualização foi detectada, reinicia o app
if st.session_state.atualizacao_pendente:
    reiniciar_test_jortform()
