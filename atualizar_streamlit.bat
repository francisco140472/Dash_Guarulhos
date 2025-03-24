@echo off
echo Finalizando processos antigos...

:: Finaliza os processos do Streamlit
tasklist | find /I "streamlit.exe" && taskkill /F /IM streamlit.exe
tasklist | find /I "python.exe" && taskkill /F /IM python.exe

echo Commitando e enviando atualizações para o GitHub...
cd C:\Users\franc\OneDrive\Documentos\ASSIS\vu_guarulhos_28022025\Dash_Guarulhos\Dash_Guarulhos
git add .
git commit -m "Atualização automática"
git push origin main

echo Atualizando repositório local...
git pull origin main

echo Iniciando Streamlit...
streamlit run test_jortform.py
