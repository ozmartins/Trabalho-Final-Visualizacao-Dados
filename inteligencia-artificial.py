import openai
import json
import os

openai.api_key = os.getenv('OPEN_AI_KEY')

with open(f'./datasets/tratados/2024.1.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
    mensagem = f"Considere este JSON: {json.dumps(dataset)}. Quais times venceram os?"
    response = openai.ChatCompletion.create(
        model = "gpt-4o-mini",
        messages = [
            { "role": "system", "content": "Você é um assistente de IA útil" },
            { "role": "user", "content": mensagem }
        ]
    )
    print(response['choices'][0]['message']['content'])