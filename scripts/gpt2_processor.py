#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesador GPT-2 en español para el chatbot
"""

import sys
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

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
    """Genera una respuesta usando GPT-2"""
    try:
        # Usar prompts más simples y directos
        simple_prompts = [
            f"Pregunta: {prompt}\nRespuesta:",
            f"Usuario dice: {prompt}\nBot responde:",
            f"Conversación:\nUsuario: {prompt}\nBot:"
        ]
        
        import random
        enhanced_prompt = random.choice(simple_prompts)
        
        # Codificación del prompt
        input_ids = tokenizer(enhanced_prompt, return_tensors="pt")
        
        # Generar el texto con parámetros conservadores
        with torch.no_grad():
            output = model.generate(
                **input_ids,
                max_length=min(max_length + len(input_ids[0]), 150),  # Limitar longitud
                temperature=max(temperature, 0.3),  # Temperatura mínima más alta
                top_p=max(top_p, 0.8),  # Top-p más conservador
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                num_return_sequences=1,
                repetition_penalty=1.5,  # Más penalización por repetición
                no_repeat_ngram_size=2,   # N-gramas más pequeños
                early_stopping=True,
                max_new_tokens=50  # Limitar tokens nuevos
            )
        
        # Decodificar la respuesta
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Limpiar la respuesta (remover el prompt original)
        response = generated_text[len(enhanced_prompt):].strip()
        
        # Limpiar caracteres extraños y mejorar formato
        response = response.replace("Usuario:", "").replace("Bot:", "").replace("Respuesta:", "").strip()
        
        # Limpiar caracteres extraños específicos
        import re
        response = re.sub(r'[^\w\s\.,!?¿¡áéíóúüñÁÉÍÓÚÜÑ]', '', response)
        
        # Si la respuesta está vacía, muy corta o contiene caracteres extraños, usar fallback
        if len(response) < 10 or '' in response or len(response.split()) > 100:
            fallback_responses = [
                f"Hola! Has escrito: '{prompt}'. ¿En qué puedo ayudarte?",
                f"Entiendo tu mensaje sobre '{prompt}'. ¿Podrías contarme más?",
                f"Interesante lo que dices: '{prompt}'. ¿Qué te gustaría saber?",
                f"Gracias por tu mensaje: '{prompt}'. ¿Hay algo específico que te interese?",
                f"He recibido: '{prompt}'. ¿En qué más puedo asistirte?",
                f"Comprendo tu punto: '{prompt}'. ¿Quieres que conversemos sobre esto?",
                f"Perfecto, has dicho: '{prompt}'. ¿Qué opinas sobre este tema?",
                f"Excelente mensaje: '{prompt}'. ¿Te gustaría profundizar en algo?"
            ]
            response = random.choice(fallback_responses)
        
        # Limitar longitud final
        if len(response) > 200:
            response = response[:200] + "..."
        
        return response
    except Exception as e:
        print(f"Error generando respuesta: {e}", file=sys.stderr)
        return f"Hola! He recibido tu mensaje: '{prompt}'. ¿En qué puedo ayudarte hoy?"

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
        "timestamp": torch.datetime.now().isoformat() if hasattr(torch, 'datetime') else "2024-01-01T00:00:00"
    }
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()

