#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que el sistema GPT-2 funciona correctamente
"""

import sys
import json
import subprocess
import os

def test_gpt2_script():
    """Prueba el script de GPT-2"""
    print("🧪 Probando script GPT-2...")
    
    script_path = os.path.join(os.path.dirname(__file__), 'gpt2_processor.py')
    if not os.path.exists(script_path):
        print("❌ Script GPT-2 no encontrado")
        return False
    
    try:
        # Ejecutar el script con un prompt de prueba
        result = subprocess.run([
            sys.executable, script_path, 
            "dime 5 videojuegos populares"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if 'response' in response:
                    print("✅ Script GPT-2 funciona correctamente")
                    print(f"   Respuesta de prueba: {response['response'][:100]}...")
                    return True
                else:
                    print("❌ Respuesta del script GPT-2 no tiene formato esperado")
                    return False
            except json.JSONDecodeError:
                print("❌ Error parseando respuesta JSON del script GPT-2")
                return False
        else:
            print(f"❌ Script GPT-2 falló con código {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Script GPT-2 tardó demasiado (timeout)")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando script GPT-2: {e}")
        return False

def test_sentiment_script():
    """Prueba el script de análisis de sentimientos"""
    print("🧪 Probando script de análisis de sentimientos...")
    
    script_path = os.path.join(os.path.dirname(__file__), 'sentiment_analyzer.py')
    if not os.path.exists(script_path):
        print("❌ Script de sentimientos no encontrado")
        return False
    
    try:
        # Ejecutar el script con un texto de prueba
        result = subprocess.run([
            sys.executable, script_path, 
            "es bonito este restaurante"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if 'sentiment' in response:
                    print("✅ Script de sentimientos funciona correctamente")
                    print(f"   Sentimiento detectado: {response['sentiment']}")
                    print(f"   Confianza: {response.get('confidence', 0):.2f}")
                    return True
                else:
                    print("❌ Respuesta del script de sentimientos no tiene formato esperado")
                    return False
            except json.JSONDecodeError:
                print("❌ Error parseando respuesta JSON del script de sentimientos")
                return False
        else:
            print(f"❌ Script de sentimientos falló con código {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Script de sentimientos tardó demasiado (timeout)")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando script de sentimientos: {e}")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'transformers',
        'torch', 
        'pysentimiento',
        'spacy',
        'nltk',
        'gensim',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} instalado")
        except ImportError:
            print(f"❌ {package} no encontrado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Paquetes faltantes: {', '.join(missing_packages)}")
        print("Ejecuta: python scripts/install_dependencies.py")
        return False
    else:
        print("✅ Todas las dependencias están instaladas")
        return True

def main():
    """Función principal de prueba"""
    print("🚀 Verificando sistema GPT-2...")
    print("=" * 50)
    
    # Verificar dependencias
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Instala las dependencias antes de continuar")
        return
    
    print("\n" + "=" * 50)
    
    # Probar scripts
    gpt2_ok = test_gpt2_script()
    
    print("\n" + "=" * 30)
    
    sentiment_ok = test_sentiment_script()
    
    print("\n" + "=" * 50)
    
    if gpt2_ok and sentiment_ok:
        print("🎉 ¡Sistema GPT-2 funcionando correctamente!")
        print("\nPara usar el chatbot:")
        print("1. Ejecuta: npm run dev")
        print("2. Ve a http://localhost:3000")
        print("3. Escribe 'hola' para comenzar")
    else:
        print("❌ Hay problemas con el sistema")
        if not gpt2_ok:
            print("   - Script GPT-2 tiene problemas")
        if not sentiment_ok:
            print("   - Script de sentimientos tiene problemas")

if __name__ == "__main__":
    main()

