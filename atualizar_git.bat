@echo off
cd /d C:\Users\franc\OneDrive\Documentos\GitHub\Dash_Guarulhos

:: Atualiza o repositório Git
git pull origin main

:: Inicia o Streamlit sem fechar o terminal
start "" C:\Users\franc\OneDrive\Documentos\GitHub\Dash_Guarulhos\.venv\Scripts\python.exe -m streamlit run test_jortform.py

exit
