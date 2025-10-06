@echo off
echo Instalando dependencias para Windows...
echo ======================================

echo.
echo 1. Instalando PyTorch para CPU...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo.
echo 2. Instalando dependencias basicas...
pip install transformers>=4.21.0
pip install pysentimiento>=0.1.4
pip install spacy>=3.4.0
pip install nltk>=3.8.0

echo.
echo 3. Instalando numpy y scipy (versiones pre-compiladas)...
pip install "numpy<2.0.0" --only-binary=all
pip install "scipy>=1.7.0" --only-binary=all

echo.
echo 4. Intentando instalar gensim...
pip install gensim>=4.2.0 --only-binary=all
if %errorlevel% neq 0 (
    echo Gensim fallo, instalando alternativa...
    pip install scikit-learn>=1.1.0 --only-binary=all
)

echo.
echo 5. Instalando utilidades...
pip install pathlib2>=2.3.0
pip install typing-extensions>=4.0.0

echo.
echo 6. Descargando modelo de spaCy...
python -m spacy download es_core_news_sm

echo.
echo ======================================
echo Instalacion completada!
echo.
echo Para usar el chatbot:
echo 1. Ejecuta: npm run dev
echo 2. Ve a http://localhost:3000
echo 3. Escribe 'hola' para comenzar
echo.
pause
