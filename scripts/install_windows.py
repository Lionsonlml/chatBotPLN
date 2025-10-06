#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalación de dependencias para Windows (evita problemas de compilación)
"""

import subprocess
import sys
import os

def install_package(package, use_precompiled=True):
    """Instala un paquete usando pip con opciones para Windows"""
    try:
        cmd = [sys.executable, "-m", "pip", "install", package]
        
        # Para Windows, usar paquetes pre-compilados cuando sea posible
        if use_precompiled:
            cmd.extend(["--only-binary=all", "--prefer-binary"])
        
        subprocess.check_call(cmd)
        print(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package}: {e}")
        return False

def install_torch_windows():
    """Instala PyTorch específicamente para Windows"""
    try:
        # Instalar PyTorch con CUDA (o CPU si no hay GPU)
        torch_cmd = [
            sys.executable, "-m", "pip", "install", 
            "torch", "torchvision", "torchaudio", 
            "--index-url", "https://download.pytorch.org/whl/cpu"
        ]
        subprocess.check_call(torch_cmd)
        print("✅ PyTorch instalado correctamente para CPU")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando PyTorch: {e}")
        return False

def install_numpy_scipy():
    """Instala numpy y scipy con paquetes pre-compilados"""
    packages = [
        "numpy<2.0.0",  # Evitar numpy 2.0 que causa problemas
        "scipy>=1.7.0"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package, use_precompiled=True):
            success_count += 1
    
    return success_count == len(packages)

def install_gensim_alternative():
    """Instala gensim o una alternativa si falla"""
    try:
        # Intentar instalar gensim primero
        if install_package("gensim>=4.2.0", use_precompiled=True):
            return True
    except:
        pass
    
    try:
        # Si gensim falla, instalar una alternativa más ligera
        print("⚠️ Gensim falló, instalando alternativa...")
        if install_package("scikit-learn>=1.1.0", use_precompiled=True):
            print("✅ Alternativa a gensim instalada")
            return True
    except:
        pass
    
    print("❌ No se pudo instalar gensim ni alternativa")
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
    """Función principal de instalación para Windows"""
    print("🚀 Instalando dependencias para Windows...")
    print("=" * 50)
    
    # 1. Instalar PyTorch primero (más crítico)
    print("📦 Instalando PyTorch...")
    torch_ok = install_torch_windows()
    
    # 2. Instalar numpy y scipy con paquetes pre-compilados
    print("\n📦 Instalando numpy y scipy...")
    numpy_scipy_ok = install_numpy_scipy()
    
    # 3. Instalar dependencias básicas
    print("\n📦 Instalando dependencias básicas...")
    basic_packages = [
        "transformers>=4.21.0",
        "pysentimiento>=0.1.4",
        "spacy>=3.4.0",
        "nltk>=3.8.0",
        "pathlib2>=2.3.0",
        "typing-extensions>=4.0.0"
    ]
    
    basic_success = 0
    for package in basic_packages:
        if install_package(package, use_precompiled=True):
            basic_success += 1
    
    # 4. Instalar gensim o alternativa
    print("\n📦 Instalando gensim...")
    gensim_ok = install_gensim_alternative()
    
    # 5. Descargar modelo de spaCy
    print("\n🌍 Descargando modelo de spaCy...")
    spacy_ok = download_spacy_model()
    
    print("\n" + "=" * 50)
    print("📊 Resumen de instalación:")
    print(f"   PyTorch: {'✅' if torch_ok else '❌'}")
    print(f"   NumPy/SciPy: {'✅' if numpy_scipy_ok else '❌'}")
    print(f"   Dependencias básicas: {basic_success}/{len(basic_packages)}")
    print(f"   Gensim: {'✅' if gensim_ok else '❌'}")
    print(f"   Modelo spaCy: {'✅' if spacy_ok else '❌'}")
    
    if torch_ok and basic_success >= len(basic_packages) - 2:  # Permitir 2 fallos
        print("\n🎉 Instalación completada exitosamente!")
        print("\nPara probar el sistema:")
        print("1. Ejecuta: npm run dev")
        print("2. Ve a http://localhost:3000")
        print("3. Escribe 'hola' para comenzar")
    else:
        print("\n❌ Hubo problemas en la instalación")
        print("\nSoluciones alternativas:")
        print("1. Instala Visual Studio Build Tools")
        print("2. O usa: conda install numpy scipy gensim")
        print("3. O instala manualmente: pip install --only-binary=all <paquete>")

if __name__ == "__main__":
    main()
