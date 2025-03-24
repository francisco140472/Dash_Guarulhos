@echo off
echo Finalizando processos antigos...

:: Finaliza os processos Streamlit e Python, caso estejam rodando
taskkill /F /IM streamlit.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1

echo Atualizando repositório...
git pull origin main

echo Verificando os últimos commits...
git log -5 --oneline

:: Ativando ambiente virtual (se necessário)
echo Ativando ambiente virtual...
call C:\Users\franc\OneDrive\Documentos\ASSIS\vu_guarulhos_28022025\Dash_Guarulhos\Dash_Guarulhos\test_jortform.py

echo Iniciando Streamlit...
streamlit run test_jortform.py
