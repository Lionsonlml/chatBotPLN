#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba directo para GPT-2 - Igual a tu código de ejemplo
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("Cargando modelo GPT-2 en español...")
nombre_modelo = "datificate/gpt2-small-spanish"

# Cargar el tokenizer y el modelo
tokenizer = AutoTokenizer.from_pretrained(nombre_modelo)
model = AutoModelForCausalLM.from_pretrained(nombre_modelo)

print("Modelo cargado exitosamente!")
print()

# Probar con varios prompts
prompts = [
    "dime 5 videojuegos",
    "hola",
    "me gustan los mariscos",
    "ayudame diciendome 5 videojuegos",
    "estoy feliz de jugar"
]

for prompt in prompts:
    print(f"Prompt: '{prompt}'")
    print("-" * 50)
    
    # Codificación del prompt
    input_tokens = tokenizer(prompt, return_tensors="pt")
    
    # Generar el texto con parámetros anti-repetición
    input_length = input_tokens['input_ids'].shape[1]
    
    output = model.generate(
        **input_tokens,
        max_new_tokens=50,  # Limitar tokens nuevos
        temperature=0.7,  # Más variedad
        top_p=0.9,
        top_k=50,  # Limitar vocabulario
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        repetition_penalty=2.0,  # Penalizar repeticiones
        no_repeat_ngram_size=3,  # No repetir 3 palabras seguidas
        early_stopping=True
    )
    
    # Decodificar
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    print(f"Respuesta: {generated_text}")
    print()
    print()

