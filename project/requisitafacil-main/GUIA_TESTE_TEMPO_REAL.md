# Guia de Teste - Sistema de Tempo Real

## ✅ Status Atual
O sistema de tempo real está **FUNCIONANDO** corretamente!

### O que foi implementado:
- ✅ WebSocket conecta automaticamente em todas as páginas
- ✅ Ping/pong mantém conexão ativa
- ✅ Notificações são enviadas quando requisições são criadas
- ✅ Dashboard atualiza automaticamente
- ✅ Reconexão automática quando necessário

---

## 🧪 Como Testar

### 1. **Preparação**
```bash
# Terminal 1: Iniciar servidores
python start_servers.py

# Terminal 2: Testar automaticamente
python test_real_scenario.py
```

### 2. **Teste Manual no Navegador**

#### **Passo 1: Abrir Dashboard**
1. Abra o navegador e acesse: `http://localhost:8000/dashboard/`
2. Faça login como gestor ou almoxarife
3. Abra o console do navegador (F12 → Console)
4. Você deve ver logs como:
   ```
   🔌 Conectando WebSocket global...
   ✅ WebSocket global conectado
   ✅ Conexão WebSocket global ativa
   ```

#### **Passo 2: Criar Requisição**
1. Em outro navegador (ou aba anônima), acesse: `http://localhost:8000/requisicoes/criar/`
2. Faça login como outro usuário (almoxarife se o primeiro for gestor)
3. Crie uma nova requisição
4. Você deve ver no log do servidor:
   ```
   Notificação recebida: created - Nova requisição criada
   Broadcasting para X clientes: created
   ```

#### **Passo 3: Verificar Atualização**
1. Volte ao primeiro navegador (dashboard)
2. Você deve ver no console:
   ```
   📨 Mensagem recebida (global): created
   🔄 Atualização recebida globalmente: created
   🔄 Recarregando dashboard...
   ```
3. O dashboard deve atualizar automaticamente (sem F5)

---

## 🔍 Como Encontrar Logs

### **Console do Navegador:**
- **Chrome/Edge:** F12 → Console tab
- **Firefox:** F12 → Console tab
- **Safari:** Cmd+Option+I → Console tab

### **Log do Servidor:**
- Terminal onde roda `python start_servers.py`
- Procure por linhas como:
  ```
  Novo cliente conectado. Total: X
  Notificação recebida: created - Nova requisição criada
  Broadcasting para X clientes: created
  ```

---

## 🚨 Possíveis Problemas

### **Problema: "Broadcasting para 0 clientes"**
**Causa:** WebSocket desconectou quando você navegou para outra página
**Solução:** O novo sistema global-websocket.js mantém a conexão ativa

### **Problema: Console não mostra logs**
**Causa:** Console pode estar filtrado
**Solução:** 
1. F12 → Console
2. Clique no ícone de filtro (funnel)
3. Certifique-se que "All" está selecionado

### **Problema: Dashboard não atualiza**
**Causa:** JavaScript pode não estar carregando
**Solução:**
1. Verifique se aparecem logs no console
2. Recarregue a página (Ctrl+F5)
3. Verifique se o arquivo `global-websocket.js` está sendo carregado

---

## 📊 Indicadores de Sucesso

### **No Console do Navegador:**
```
✅ WebSocket global conectado
✅ Conexão WebSocket global ativa
📨 Mensagem recebida (global): created
🔄 Atualização recebida globalmente: created
🔄 Recarregando dashboard...
```

### **No Log do Servidor:**
```
Novo cliente conectado. Total: 1
Ping recebido e respondido. Clientes ativos: 1
Notificação recebida: created - Nova requisição criada
Broadcasting para 1 clientes: created
Mensagem enviada para cliente
```

---

## 🎯 Resultado Esperado

Quando você criar uma requisição em um navegador, o dashboard em outro navegador deve:
1. ✅ Mostrar notificação visual
2. ✅ Atualizar automaticamente (sem F5)
3. ✅ Exibir a nova requisição na lista
4. ✅ Atualizar os contadores dos cards

---

## 🔧 Arquivos Modificados

- `static/core/global-websocket.js` - WebSocket global
- `static/core/dashboard-realtime.js` - WebSocket específico do dashboard
- `templates/base.html` - Inclui script global
- `realtime_server.py` - Servidor FastAPI melhorado

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique se ambos os servidores estão rodando
2. Confirme se os logs aparecem no console
3. Teste com `python test_real_scenario.py`
4. Envie os logs do console e do servidor para análise 