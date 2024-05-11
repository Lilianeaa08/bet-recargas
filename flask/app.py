from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import pytz
from botGen import bot_recargas
import re

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client['bot_atendimento']
collection = db['chat_recargas']


def ajuste_texto(text):
    parágrafos = re.split(r'(\d+\.\s)', text)
    texto_formatado = ''
    for i in range(len(parágrafos)):
        if i % 2 == 0:
            texto_formatado += parágrafos[i]
        else:
            texto_formatado += f'<br><br>{parágrafos[i]}'
    return texto_formatado

def link_formatado(text):
    url_pattern = re.compile(r'(https?://\S+)')
    return url_pattern.sub(r'<a href="\1">\1</a>', text)

def getCurrentTime():
    now_utc = datetime.utcnow()
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    now_brasilia = now_utc.replace(tzinfo=pytz.utc).astimezone(brasilia_tz)
    formatted_time = now_brasilia.strftime("%Y/%m/%d %H:%M")
    return formatted_time

def formatBotMessage(message):
    message_parts = message.split('*')
    formatted_message_parts = [' '.join(part.strip() for part in message_parts)]
    formatted_message = '<br>'.join(formatted_message_parts)
    formatted_message = formatted_message.replace('**', '<br><br>')
    formatted_message = link_formatado(formatted_message)
    formatted_message = ajuste_texto(formatted_message)
    return formatted_message

def iniciar_nova_sessao():
    collection.insert_one({'user': [], 'bot': []})

@app.route('/')
def index():
    iniciar_nova_sessao()
    mensagem_bot = "Seja bem vindo a⚡Bet Recargas! 🚗"
    return render_template('bet_recargas.html', mensagem_bot=mensagem_bot, getCurrentTime=getCurrentTime,bot_recargas= bot_recargas, link_formatado = link_formatado)

@app.route('/bot_response', methods=['POST'])
def bot_response():
    input_usuario = request.json['input']
    resposta_bot = bot_recargas(input_usuario)
    resposta_formatada = formatBotMessage(resposta_bot)
    return jsonify({'response': resposta_formatada})

@app.route('/encerrar_chat', methods=['POST'])
def encerrar_chat():
    chat_history = request.json['chatHistory']
    collection.insert_one({'user': chat_history['user'], 'bot': chat_history['bot']})
    return jsonify({'message': 'Chat encerrado e histórico salvo com sucesso!'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5171)
