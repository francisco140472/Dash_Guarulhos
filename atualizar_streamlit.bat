@echo off

echo Finalizando processos antigos...
tasklist | find /I "streamlit.exe" && taskkill /F /IM streamlit.exe /T
tasklist | find /I "python.exe" && taskkill /F /IM python.exe /T

echo Atualizando repositório...
git pull origin main

echo Iniciando Streamlit...
start "" C:\Users\franc\OneDrive\Documentos\ASSIS\vu_guarulhos_28022025\Dash_Guarulhos\Dash_Guarulhos\.venv\Scripts\python.exe -m streamlit run test_jortform.py --server.port 8501

exit
