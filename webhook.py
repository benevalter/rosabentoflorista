from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import json
import re
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

messages = []

def format_timestamp(timestamp):
    # Converter o timestamp UNIX para um objeto datetime
    dt_object = datetime.fromtimestamp(timestamp)
    # Formatar a data e hora para o formato brasileiro
    formatted_timestamp = dt_object.strftime('%d/%m/%Y %H:%M:%S')
    return formatted_timestamp

def extract_links(message_body):
    # Utilizar expressão regular para encontrar links no texto
    regex = r'(https?://\S+)'
    links = re.findall(regex, message_body)
    return links

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Receber dados da mensagem do WhatsApp
        data = request.json
        
        # Extrair os detalhes da mensagem
        from_number = data.get('from')
        to_number = data.get('to')
        message_body = data.get('body')
        image = data.get('image')
        timestamp = data.get('timestamp')
        author_name = data.get('authorName', 'Desconhecido')  # Adicionando o nome do autor
        
        # Verificar se há links no corpo da mensagem
        links = extract_links(message_body)
        for link in links:
            # Substituir o link no texto pelo link ativo
            message_body = message_body.replace(link, f'<a href="{link}" target="_blank">{link}</a>')
        
        # Formatar o timestamp
        formatted_timestamp = format_timestamp(timestamp)
        
        # Criar a mensagem formatada
        message = f'Image: {image}, Autor: {author_name}, Mensagem de: {from_number}, Para: {to_number}, Conteúdo: {message_body}, Timestamp: {formatted_timestamp}'
        
        # Adicionar a mensagem à lista de mensagens
        messages.append(message)
        print(message)
        
        # Emitir a mensagem para os clientes conectados via Socket.IO
        socketio.emit('update_messages', message)
        
        # Retornar uma resposta de sucesso
        return jsonify({'success': True}), 200
    else:
        # Renderizar a página HTML com as mensagens existentes
        return render_template('chat.html', messages=messages)

if __name__ == '__main__':
    socketio.run(app, port=5000)
