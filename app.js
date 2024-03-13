const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

// Configurações do cliente WhatsApp
const client = new Client();

// Evento quando o cliente está pronto
client.on('qr', qr => {
    // Exibir QR code no terminal
    qrcode.generate(qr, { small: true });
});

// Evento quando o cliente está autenticado
client.on('authenticated', (session) => {
    console.log('Autenticado com sucesso!');
});

// Evento quando uma mensagem é recebida
client.on('message', async (message) => {
    let authorName = 'Desconhecido';
    if (message.isGroupMsg) {
        authorName = message.author || 'Desconhecido';
    } else {
        const contact = await message.getContact();
        authorName = contact.name || 'Desconhecido';
    }
    // Enviar os dados da mensagem para o seu próprio webhook
    try {
        await axios.post('https://benevalter.app.n8n.cloud/webhook/69815a1a-e479-4b3c-9369-ac77d6a0a37d', {
            from: message.from,
            to: message.to,
            body: message.body,
            image: message.hasMedia ? message.body : null,
            timestamp: message.timestamp,
            authorName: authorName // Adicionando o nome do autor
            // Adicione outras propriedades da mensagem conforme necessário
        });
        console.log('Dados da mensagem enviados para o seu webhook com sucesso!');
    } catch (error) {
        console.error('Erro ao enviar dados para o seu webhook:', error);
    }
});

// Iniciar o cliente
client.initialize();
