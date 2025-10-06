# Script de instalación para PowerShell
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "  INSTALACION DE DEPENDENCIAS" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Instalando PyTorch..." -ForegroundColor Yellow
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

Write-Host ""
Write-Host "2. Instalando transformers..." -ForegroundColor Yellow
pip install transformers>=4.21.0

Write-Host ""
Write-Host "3. Instalando pysentimiento..." -ForegroundColor Yellow
pip install pysentimiento>=0.1.4

Write-Host ""
Write-Host "4. Instalando spacy..." -ForegroundColor Yellow
pip install spacy>=3.4.0

Write-Host ""
Write-Host "5. Instalando nltk..." -ForegroundColor Yellow
pip install nltk>=3.8.0

Write-Host ""
Write-Host "6. Instalando numpy (version compatible)..." -ForegroundColor Yellow
pip install "numpy>=1.21.0,<2.0.0"

Write-Host ""
Write-Host "7. Instalando scipy..." -ForegroundColor Yellow
pip install "scipy>=1.7.0"

Write-Host ""
Write-Host "8. Instalando scikit-learn..." -ForegroundColor Yellow
pip install scikit-learn>=1.1.0

Write-Host ""
Write-Host "9. Instalando utilidades..." -ForegroundColor Yellow
pip install pathlib2>=2.3.0
pip install typing-extensions>=4.0.0

Write-Host ""
Write-Host "10. Descargando modelo de spaCy..." -ForegroundColor Yellow
python -m spacy download es_core_news_sm

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "  INSTALACION COMPLETADA" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para probar el sistema:" -ForegroundColor Cyan
Write-Host "1. npm install" -ForegroundColor White
Write-Host "2. npm run dev" -ForegroundColor White
Write-Host "3. Ve a http://localhost:3000" -ForegroundColor White
Write-Host "4. Escribe 'hola' para comenzar" -ForegroundColor White
Write-Host ""
Write-Host "NOTA: La primera vez que uses GPT-2, se descargara el modelo (~500 MB)" -ForegroundColor Yellow
Write-Host ""

