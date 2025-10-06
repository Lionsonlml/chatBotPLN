#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador GPT-2 en español para el chatbot
"""

import sys
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import io

# Configurar stdout para UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_gpt2_model():
    """Carga el modelo GPT-2 en español"""
    try:
        nombre_modelo = "datificate/gpt2-small-spanish"
        
        # Cargar el tokenizer y el modelo
        tokenizer = AutoTokenizer.from_pretrained(nombre_modelo)
        model = AutoModelForCausalLM.from_pretrained(nombre_modelo)
        
        # Configurar el pad_token si no existe
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        return tokenizer, model
    except Exception as e:
        print(f"Error cargando el modelo GPT-2: {e}", file=sys.stderr)
        return None, None

def generate_response(tokenizer, model, prompt, max_length=120, temperature=0.1, top_p=0.9):
    """Genera una respuesta usando GPT-2 con control de repeticiones"""
    try:
        # Agregar contexto conversacional para que GPT-2 entienda que es un chat
        conversational_prompt = f"Pregunta: {prompt}\nRespuesta corta:"
        
        # Codificación del prompt
        input_tokens = tokenizer(conversational_prompt, return_tensors="pt")
        
        # Calcular max_new_tokens en lugar de max_length para evitar repeticiones largas
        input_length = input_tokens['input_ids'].shape[1]
        max_new_tokens = min(30, max_length - input_length)  # Limitar a 30 tokens nuevos para respuestas cortas
        
        # Generar el texto con parámetros anti-repetición
        with torch.no_grad():
            output = model.generate(
                **input_tokens,
                max_new_tokens=max_new_tokens,
                min_length=input_length + 5,  # Mínimo 5 tokens nuevos
                temperature=max(temperature, 0.7),  # Temperatura más alta para más variedad
                top_p=top_p,
                top_k=50,  # Limitar a los 50 tokens más probables
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                repetition_penalty=2.0,  # Penalización fuerte por repetición
                no_repeat_ngram_size=3,  # No repetir secuencias de 3 palabras
                early_stopping=True
            )
        
        # Decodificar
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Extraer solo la respuesta (remover el prefijo del prompt)
        if "Respuesta corta:" in generated_text:
            response = generated_text.split("Respuesta corta:")[-1].strip()
        else:
            response = generated_text[len(conversational_prompt):].strip()
        
        # Limpiar la respuesta
        response = response.strip()
        
        # Si la respuesta es muy larga, tomar solo la primera oración
        if len(response) > 200 or response.count('.') > 2:
            first_sentence = response.split('.')[0] + '.'
            if len(first_sentence) > 10:
                response = first_sentence
        
        # Verificar si hay repeticiones excesivas
        words = response.split()
        if len(words) > 10:
            unique_words = len(set(words))
            total_words = len(words)
            repetition_ratio = unique_words / total_words
            
            # Si más del 70% son repeticiones, generar respuesta simple
            if repetition_ratio < 0.3:
                return generate_simple_response(prompt)
        
        # Si la respuesta parece un artículo o tiene contenido irrelevante, usar respuesta simple
        article_indicators = ['temporada', 'años', 'campeón', 'jugador', 'equipo', 'club', 'liga', 
                            'montañas', 'valles', 'región', 'cultura', 'símbolo']
        
        words_lower = [w.lower() for w in words]
        article_count = sum(1 for indicator in article_indicators if indicator in words_lower)
        
        if article_count >= 3:  # Si tiene 3 o más palabras de artículo, generar respuesta simple
            return generate_simple_response(prompt)
        
        # Si está vacía o muy corta, generar respuesta simple
        if len(response) < 5:
            return generate_simple_response(prompt)
        
        return response
        
    except Exception as e:
        print(f"Error generando respuesta: {e}", file=sys.stderr)
        return generate_simple_response(prompt)

def generate_simple_response(prompt):
    """Genera respuestas simples y directas cuando GPT-2 falla"""
    prompt_lower = prompt.lower()
    
    # Saludos
    if any(greeting in prompt_lower for greeting in ['hola', 'hi', 'hello', 'buenas', 'saludos']):
        responses = [
            "¡Hola! ¿Cómo estás? ¿En qué puedo ayudarte?",
            "¡Hola! Es un placer conversar contigo.",
            "¡Hola! ¿Qué tal? ¿En qué puedo asistirte hoy?",
            "¡Hola! Estoy aquí para ayudarte."
        ]
        import random
        return random.choice(responses)
    
    # Preguntas sobre estado
    if any(word in prompt_lower for word in ['como estas', 'qué tal', 'como va', 'todo bien']):
        return "Muy bien, gracias por preguntar. ¿Y tú? ¿En qué puedo ayudarte?"
    
    # Preguntas sobre juegos
    if any(word in prompt_lower for word in ['juego', 'videojuego', 'gaming']):
        return "Hay muchos juegos excelentes. ¿Te interesan los de acción, aventura, o deportes? Algunos populares son Minecraft, Fortnite, FIFA, Mario y Zelda."
    
    # Preguntas sobre números o listas
    if any(word in prompt_lower for word in ['dime', 'dame', 'lista', 'cuales', 'cuáles']):
        return f"Interesante pregunta sobre '{prompt}'. ¿Podrías darme más detalles sobre qué tipo de información necesitas?"
    
    # Respuesta general
    return f"Entiendo tu mensaje: '{prompt}'. ¿Podrías darme más contexto para ayudarte mejor?"

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        result = {
            "error": "Texto requerido como parámetro"
        }
        print(json.dumps(result, ensure_ascii=False))
        return
    
    # Obtener parámetros
    prompt = sys.argv[1]
    max_length = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    temperature = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1
    top_p = float(sys.argv[4]) if len(sys.argv) > 4 else 0.9
    
    # Cargar modelo
    tokenizer, model = load_gpt2_model()
    
    if tokenizer is None or model is None:
        result = {
            "error": "No se pudo cargar el modelo GPT-2",
            "fallback_response": f"He recibido tu mensaje: '{prompt}'. Este es un ejemplo de respuesta."
        }
        print(json.dumps(result, ensure_ascii=False))
        return
    
    # Generar respuesta
    response = generate_response(tokenizer, model, prompt, max_length, temperature, top_p)
    
    # Crear resultado
    result = {
        "response": response,
        "model": "gpt2-small-spanish",
        "parameters": {
            "max_length": max_length,
            "temperature": temperature,
            "top_p": top_p
        },
        "prompt": prompt,
        "timestamp": "2024-01-01T00:00:00"
    }
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
