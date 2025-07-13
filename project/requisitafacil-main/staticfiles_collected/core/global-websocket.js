// Global WebSocket Manager
// Mantém a conexão WebSocket ativa em todas as páginas do sistema

(function() {
    'use strict';
    
    let ws = null;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    
    function connectWebSocket() {
        if (ws && ws.readyState === WebSocket.OPEN) {
            return; // Já está conectado
        }
        
        console.log('🔌 Conectando WebSocket global...');
        ws = new WebSocket('ws://localhost:8001/ws/updates');
        
        ws.onopen = function() {
            console.log('✅ WebSocket global conectado');
            reconnectAttempts = 0;
            
            // Envia ping inicial
            ws.send('ping');
            
            // Configura ping periódico
            setInterval(() => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send('ping');
                }
            }, 30000); // Ping a cada 30 segundos
        };
        
        ws.onmessage = function(event) {
            console.log('📨 Mensagem recebida (global):', event.data);
            
            // Se recebeu pong, a conexão está ativa
            if (event.data === 'pong') {
                console.log('✅ Conexão WebSocket global ativa');
                return;
            }
            
            // Se recebeu notificação de atualização
            if (event.data === 'created' || event.data === 'finalized' || event.data === 'update') {
                console.log('🔄 Atualização recebida globalmente:', event.data);
                
                // Mostra notificação visual
                showGlobalNotification('Nova atualização no sistema!', 'info');
                
                // Se estiver na página do dashboard, recarrega
                if (window.location.pathname.includes('/dashboard')) {
                    console.log('🔄 Recarregando dashboard...');
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                }
            }
        };
        
        ws.onerror = function(error) {
            console.error('❌ Erro no WebSocket global:', error);
        };
        
        ws.onclose = function() {
            console.log('🔌 WebSocket global desconectado');
            
            // Tenta reconectar se não excedeu o limite
            if (reconnectAttempts < maxReconnectAttempts) {
                reconnectAttempts++;
                console.log(`🔄 Tentativa de reconexão ${reconnectAttempts}/${maxReconnectAttempts}...`);
                setTimeout(connectWebSocket, 3000);
            } else {
                console.log('❌ Máximo de tentativas de reconexão atingido');
            }
        };
    }
    
    function showGlobalNotification(message, type = 'info') {
        // Remove notificações antigas
        const existingNotifications = document.querySelectorAll('.global-notification');
        existingNotifications.forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = 'global-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            z-index: 9999;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease-out;
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
        
        // Remove após 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    // Adiciona CSS para animação
    if (!document.getElementById('global-websocket-styles')) {
        const style = document.createElement('style');
        style.id = 'global-websocket-styles';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Inicia a conexão quando o DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', connectWebSocket);
    } else {
        connectWebSocket();
    }
    
    // Reconecta quando a página volta a ficar visível
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden && ws && ws.readyState === WebSocket.CLOSED) {
            console.log('🔄 Reconectando WebSocket após retorno à página...');
            reconnectAttempts = 0;
            connectWebSocket();
        }
    });
    
    // Expõe funções para uso global
    window.WebSocketManager = {
        connect: connectWebSocket,
        showNotification: showGlobalNotification
    };
    
})(); 