@echo off
echo Finalizando processos antigos...

:: Finaliza apenas se os processos existirem
tasklist | find /I "streamlit.exe" && taskkill /F /IM streamlit.exe
tasklist | find /I "python.exe" && taskkill /F /IM python.exe

echo Atualizando repositório...
git pull origin main

echo Verificando os últimos commits...
git log -5 --oneline

echo Iniciando Streamlit...
streamlit run test_jortform.py
