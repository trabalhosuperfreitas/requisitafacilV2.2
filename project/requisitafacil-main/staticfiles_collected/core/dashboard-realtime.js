// Dashboard Real-time Updates
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard Real-time JS carregado');
    
    // Conecta ao WebSocket do FastAPI
    const ws = new WebSocket('ws://localhost:8001/ws/updates');
    
    // Mantém a conexão ativa mesmo quando a página perde foco
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden && ws.readyState === WebSocket.CLOSED) {
            console.log('🔄 Reconectando WebSocket após retorno à página...');
            location.reload();
        }
    });
    
    ws.onopen = function() {
        console.log('✅ WebSocket conectado ao dashboard');
        // Envia uma mensagem de ping para manter a conexão ativa
        ws.send('ping');
        
        // Configura ping periódico para manter a conexão ativa
        setInterval(() => {
            if (ws.readyState === WebSocket.OPEN) {
                console.log('🔄 Enviando ping para manter conexão...');
                ws.send('ping');
            }
        }, 20000); // Ping a cada 20 segundos
    };
    
    ws.onmessage = function(event) {
        console.log('📨 Mensagem recebida no dashboard:', event.data);
        
        // Se recebeu pong, a conexão está ativa
        if (event.data === 'pong') {
            console.log('✅ Conexão WebSocket ativa');
            return;
        }
        
        // Recarrega a página quando receber uma atualização
        if (event.data === 'created' || event.data === 'finalized' || event.data === 'update') {
            console.log('🔄 Atualizando dashboard...');
            // Mostra uma notificação visual antes de recarregar
            if (typeof showNotification === 'function') {
                showNotification('Nova atualização recebida!', 'info');
            }
            setTimeout(function() {
                location.reload();
            }, 1000);
        }
    };
    
    ws.onerror = function(error) {
        console.error('❌ Erro no WebSocket:', error);
    };
    
    ws.onclose = function() {
        console.log('🔌 WebSocket desconectado do dashboard');
        // Tenta reconectar após 5 segundos
        setTimeout(function() {
            console.log('🔄 Tentando reconectar...');
            location.reload();
        }, 5000);
    };
    
    // Função para mostrar notificações (se não existir)
    if (typeof showNotification === 'undefined') {
        window.showNotification = function(message, type = 'info') {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px;
                border-radius: 5px;
                color: white;
                z-index: 9999;
                font-weight: bold;
            `;
            
            if (type === 'info') {
                notification.style.backgroundColor = '#007bff';
            } else if (type === 'success') {
                notification.style.backgroundColor = '#28a745';
            } else if (type === 'warning') {
                notification.style.backgroundColor = '#ffc107';
            } else {
                notification.style.backgroundColor = '#dc3545';
            }
            
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(function() {
                notification.remove();
            }, 3000);
        };
    }
}); 