@echo off
cd /d C:\Users\franc\OneDrive\Documentos\GitHub\Dash_Guarulhos

:: Inicia o Streamlit sem fechar o terminal
start "" "C:\Users\franc\OneDrive\Documentos\GitHub\Dash_Guarulhos\.venv\Scripts\python.exe" -m streamlit run test_jortform.py

:: Aguarda 5 segundos para garantir que o Streamlit iniciou
timeout /t 5 /nobreak

:: Atualiza o repositório Git
"C:\Users\franc\OneDrive\Documentos\GitHub\Dash_Guarulhos\.venv\Scripts\python.exe" test_jortform.py

exit
