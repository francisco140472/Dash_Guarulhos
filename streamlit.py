import os
import subprocess
import streamlit as st

# Função para atualizar o código automaticamente
def atualizar_codigo():
    try:
        # Executar Git Pull
        resultado = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
        st.sidebar.write("🔄 Atualizando código...")
        st.sidebar.write(resultado.stdout)
        if "Already up to date" in resultado.stdout:
            st.sidebar.write("✅ Código já está atualizado!")
        else:
            st.sidebar.write("⚠ Atualização aplicada, reinicie o app!")
    except Exception as e:
        st.sidebar.write(f"❌ Erro ao atualizar: {e}")

# Botão para atualizar o código na interface
if st.sidebar.button("🔄 Atualizar Código"):
    atualizar_codigo()
