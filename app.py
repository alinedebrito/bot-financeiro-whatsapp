from flask import Flask, request
import json
from datetime import datetime

app = Flask(__name__)

def load_db():
    try:
        with open('database.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_db(data):
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    phone = data['from']
    message = data['body'].lower()

    db = load_db()

    if phone not in db:
        db[phone] = []

    if "gastei" in message or "recebi" in message:
        valor = ''.join([c for c in message if c.isdigit() or c == '.'])
        tipo = 'despesa' if 'gastei' in message else 'receita'
        db[phone].append({
            'tipo': tipo,
            'valor': float(valor),
            'data': str(datetime.now())
        })
        save_db(db)
        return {"reply": f"{tipo.capitalize()} de R$ {valor} registrada com sucesso!"}

    if "saldo" in message:
        saldo = sum([i['valor'] if i['tipo'] == 'receita' else -i['valor'] for i in db[phone]])
        return {"reply": f"Seu saldo atual é R$ {saldo:.2f}"}

    return {"reply": "Comando não reconhecido. Tente: 'gastei 50 reais' ou 'saldo'"}

if __name__ == '__main__':
    app.run(debug=True) 
Adiciona app.py do bot financeiro
