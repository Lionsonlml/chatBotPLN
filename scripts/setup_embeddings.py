#!/usr/bin/env python3
"""
Script de Configuración para Embeddings Semánticos
==================================================

Este script configura el entorno necesario para el módulo de embeddings semánticos,
incluyendo la instalación de dependencias y el entrenamiento inicial del modelo.

Autor: Asistente IA
Fecha: 2024
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_requirements():
    """Instala las dependencias necesarias."""
    logger.info("Instalando dependencias...")
    
    try:
        # Instalar dependencias básicas
        subprocess.run([sys.executable, "-m", "pip", "install", "gensim", "numpy", "scipy"], check=True)
        logger.info("Dependencias básicas instaladas")
        
        # Intentar instalar spaCy
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "spacy"], check=True)
            logger.info("spaCy instalado")
        except subprocess.CalledProcessError:
            logger.warning("No se pudo instalar spaCy")
        
        # Intentar instalar modelo de español
        try:
            subprocess.run([sys.executable, "-m", "spacy", "download", "es_core_news_sm"], check=True)
            logger.info("Modelo de español descargado")
        except subprocess.CalledProcessError:
            logger.warning("No se pudo descargar el modelo de español")
            try:
                subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
                logger.info("Modelo de inglés descargado como fallback")
            except subprocess.CalledProcessError:
                logger.warning("No se pudo descargar ningún modelo de spaCy")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al instalar dependencias: {e}")
        return False

def create_directories():
    """Crea los directorios necesarios."""
    logger.info("Creando directorios...")
    
    directories = [
        "models",
        "data",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"Directorio creado: {directory}")

def test_imports():
    """Prueba las importaciones necesarias."""
    logger.info("Probando importaciones...")
    
    try:
        import gensim
        logger.info("✓ Gensim disponible")
    except ImportError:
        logger.error("✗ Gensim no disponible")
        return False
    
    try:
        import numpy
        logger.info("✓ NumPy disponible")
    except ImportError:
        logger.error("✗ NumPy no disponible")
        return False
    
    try:
        import spacy
        logger.info("✓ spaCy disponible")
    except ImportError:
        logger.warning("⚠ spaCy no disponible")
    
    return True

def train_initial_model():
    """Entrena el modelo inicial de embeddings."""
    logger.info("Entrenando modelo inicial...")
    
    try:
        # Agregar el directorio lib al path
        sys.path.append(str(Path(__file__).parent.parent / "lib"))
        
        from semantic_embeddings import SemanticEmbeddings
        
        # Crear instancia y entrenar
        embeddings = SemanticEmbeddings()
        
        if not embeddings.is_trained:
            logger.info("Modelo no encontrado, entrenando...")
            success = embeddings.train_model()
            
            if success:
                logger.info("✓ Modelo entrenado exitosamente")
                return True
            else:
                logger.error("✗ Error al entrenar el modelo")
                return False
        else:
            logger.info("✓ Modelo ya existe")
            return True
            
    except Exception as e:
        logger.error(f"Error al entrenar modelo: {e}")
        return False

def main():
    """Función principal del script."""
    logger.info("=== Configuración de Embeddings Semánticos ===")
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if not install_requirements():
        logger.error("Error en la instalación de dependencias")
        return False
    
    # Probar importaciones
    if not test_imports():
        logger.error("Error en las importaciones")
        return False
    
    # Entrenar modelo
    if not train_initial_model():
        logger.error("Error al entrenar el modelo")
        return False
    
    logger.info("=== Configuración completada exitosamente ===")
    logger.info("El módulo de embeddings semánticos está listo para usar")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
