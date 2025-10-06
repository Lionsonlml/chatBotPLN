@echo off
echo ==========================================
echo   INSTALACION SIMPLIFICADA PARA WINDOWS
echo ==========================================
echo.

echo Instalando solo las dependencias esenciales...
echo (Saltando gensim para evitar errores de compilacion)
echo.

echo 1. Instalando PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo.
echo 2. Instalando transformers...
pip install transformers>=4.21.0

echo.
echo 3. Instalando pysentimiento...
pip install pysentimiento>=0.1.4

echo.
echo 4. Instalando spacy...
pip install spacy>=3.4.0

echo.
echo 5. Instalando nltk...
pip install nltk>=3.8.0

echo.
echo 6. Instalando numpy (version compatible)...
pip install "numpy>=1.21.0,<2.0.0"

echo.
echo 7. Instalando scipy...
pip install "scipy>=1.7.0"

echo.
echo 8. Instalando scikit-learn (alternativa a gensim)...
pip install scikit-learn>=1.1.0

echo.
echo 9. Instalando utilidades...
pip install pathlib2>=2.3.0
pip install typing-extensions>=4.0.0

echo.
echo 10. Descargando modelo de spaCy...
python -m spacy download es_core_news_sm

echo.
echo ==========================================
echo   INSTALACION COMPLETADA
echo ==========================================
echo.
echo El sistema funcionara sin gensim.
echo Si necesitas gensim mas adelante, puedes instalarlo con:
echo   conda install gensim
echo   o
echo   pip install gensim --only-binary=all
echo.
echo Para probar el sistema:
echo 1. npm install
echo 2. npm run dev
echo 3. Ve a http://localhost:3000
echo 4. Escribe 'hola' para comenzar
echo.
echo NOTA: Si las respuestas de GPT-2 son raras, es normal la primera vez.
echo El modelo se descarga y ajusta automaticamente.
echo.
pause
