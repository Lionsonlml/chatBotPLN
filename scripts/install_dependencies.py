#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalación de dependencias para el chatbot GPT-2
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package}: {e}")
        return False

def download_spacy_model():
    """Descarga el modelo de spaCy para español"""
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "es_core_news_sm"])
        print("✅ Modelo de spaCy para español descargado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error descargando modelo de spaCy: {e}")
        return False

def main():
    """Función principal de instalación"""
    print("🚀 Instalando dependencias para el Chatbot GPT-2...")
    print("=" * 50)
    
    # Lista de paquetes a instalar
    packages = [
        "transformers>=4.21.0",
        "torch>=1.12.0", 
        "pysentimiento>=0.1.4",
        "spacy>=3.4.0",
        "nltk>=3.8.0",
        "gensim>=4.2.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "scikit-learn>=1.1.0",
        "pathlib2>=2.3.0",
        "typing-extensions>=4.0.0"
    ]
    
    # Instalar paquetes
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Resumen: {success_count}/{len(packages)} paquetes instalados correctamente")
    
    # Descargar modelo de spaCy
    print("\n🌍 Descargando modelo de spaCy para español...")
    if download_spacy_model():
        print("✅ Modelo de spaCy listo")
    else:
        print("❌ Error con modelo de spaCy - puedes instalarlo manualmente con:")
        print("   python -m spacy download es_core_news_sm")
    
    print("\n🎉 Instalación completada!")
    print("\nPara probar el sistema:")
    print("1. Ejecuta: npm run dev")
    print("2. Ve a http://localhost:3000")
    print("3. Escribe 'hola' para comenzar a conversar con GPT-2")

if __name__ == "__main__":
    main()

