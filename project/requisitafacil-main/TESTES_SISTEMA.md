# 🧪 Sistema de Testes - Requisição Fácil

Este documento explica como usar o sistema de testes para verificar se todas as funcionalidades estão funcionando corretamente, incluindo a atualização dos cards de KPI do gestor.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Como Executar os Testes](#como-executar-os-testes)
3. [Gerando Dados de Teste](#gerando-dados-de-teste)
4. [Testes Disponíveis](#testes-disponíveis)
5. [Verificando KPIs do Gestor](#verificando-kpis-do-gestor)
6. [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

O sistema de testes foi criado para:

- ✅ Gerar requisições falsas automaticamente
- ✅ Verificar se todas as funcionalidades estão funcionando
- ✅ Testar a atualização dos cards de KPI do gestor
- ✅ Validar permissões de usuários
- ✅ Testar fluxos completos de requisições
- ✅ Verificar estatísticas e gráficos

## 🚀 Como Executar os Testes

### Opção 1: Script Interativo (Recomendado)

```bash
python testar_sistema.py
```

Este script oferece um menu interativo com as seguintes opções:

1. **Gerar dados de teste (50 requisições)**
2. **Gerar dados de teste (100 requisições)**
3. **Gerar dados de teste (200 requisições)**
4. **Executar testes completos**
5. **Executar testes rápidos**
6. **Mostrar estatísticas**
7. **Limpar dados de teste**
8. **Executar tudo (gerar dados + testes)**

### Opção 2: Comandos Django Diretos

#### Gerar dados de teste:
```bash
python manage.py gerar_dados_teste --num-requisicoes 100
```

#### Executar testes:
```bash
python manage.py test core.tests.RequisicaoFacilTestCase
```

#### Executar testes específicos:
```bash
python manage.py test core.tests.RequisicaoFacilTestCase.test_kpis_gestor_apos_criar_requisicoes
```

## 📊 Gerando Dados de Teste

### Comando Básico
```bash
python manage.py gerar_dados_teste
```

### Opções Disponíveis

- `--num-requisicoes`: Número de requisições a criar (padrão: 100)
- `--setores`: Lista de setores (padrão: todos os setores)
- `--dias-atras`: Dias para trás para criar requisições (padrão: 30)

### Exemplos

```bash
# Criar 50 requisições
python manage.py gerar_dados_teste --num-requisicoes 50

# Criar 200 requisições nos últimos 15 dias
python manage.py gerar_dados_teste --num-requisicoes 200 --dias-atras 15

# Criar requisições apenas para setores específicos
python manage.py gerar_dados_teste --setores FLV Frios Padaria
```

## 🧪 Testes Disponíveis

### 1. Teste de Criação de Requisições Falsas
```python
test_criar_requisicoes_fake_para_todos_setores()
```
- Cria requisições para todos os setores
- Testa diferentes status (Pendente, Em Atendimento, Aprovada)
- Verifica geração de códigos de requisição

### 2. Teste de KPIs do Gestor
```python
test_kpis_gestor_apos_criar_requisicoes()
```
- Verifica se os KPIs são calculados corretamente
- Testa contadores de requisições pendentes, aprovadas, etc.
- Valida estatísticas por setor

### 3. Teste de Fluxo Completo
```python
test_fluxo_completo_requisicao()
```
- Simula criação de requisição por encarregado
- Testa atendimento por almoxarife
- Verifica finalização da requisição

### 4. Teste de Permissões
```python
test_permissoes_usuarios()
```
- Verifica acesso correto aos dashboards
- Testa restrições de permissão
- Valida roles de usuários

### 5. Teste de Atualização em Tempo Real
```python
test_atualizacao_kpis_tempo_real()
```
- Verifica se KPIs são atualizados após novas requisições
- Testa contadores dinâmicos

### 6. Teste de Estatísticas por Setor
```python
test_estatisticas_por_setor()
```
- Valida gráficos de setores
- Testa distribuição por status
- Verifica dados para visualizações

### 7. Teste de Requisições Urgentes
```python
test_requisicoes_urgentes()
```
- Verifica tratamento de requisições urgentes
- Testa contadores específicos

### 8. Teste de Tempo Médio
```python
test_tempo_medio_atendimento()
```
- Calcula tempo médio de atendimento
- Verifica formatação de tempo

### 9. Teste de Percentual no Prazo
```python
test_percentual_atendidas_prazo()
```
- Calcula percentual de requisições atendidas no prazo
- Testa métricas de performance

### 10. Teste de Stress
```python
test_criar_muitas_requisicoes_fake()
```
- Cria muitas requisições para testar performance
- Verifica comportamento com grande volume de dados

## 📈 Verificando KPIs do Gestor

### KPIs Testados

1. **Requisições Pendentes**: Contador de requisições com status "Pendente"
2. **Requisições Aprovadas Hoje**: Contador de requisições aprovadas no dia atual
3. **Total do Mês**: Contador de requisições criadas no mês atual
4. **Departamentos Ativos**: Número de setores com requisições
5. **Requisições Urgentes Pendentes**: Contador de requisições urgentes pendentes
6. **Tempo Médio de Atendimento**: Tempo médio para aprovar requisições
7. **Percentual no Prazo**: % de requisições atendidas em até 24h

### Como Verificar Manualmente

1. **Acesse o sistema**: http://localhost:8000
2. **Faça login como gestor**: `gestor_teste` / `testpass123`
3. **Acesse o dashboard do gestor**
4. **Verifique os cards de KPI**:
   - Pendentes
   - Aprovadas hoje
   - Total do mês
   - Departamentos ativos
   - Urgentes pendentes

### Dados de Teste Gerados

O sistema gera dados realistas com:

- **Distribuição de Status**:
  - 30% Pendentes
  - 20% Em Atendimento
  - 50% Aprovadas

- **Distribuição de Urgência**:
  - 80% Normal
  - 20% Urgente

- **Itens Diversos**:
  - 30 tipos diferentes de itens
  - Quantidades variadas (1-20)
  - Categorias variadas

## 🔧 Troubleshooting

### Problema: "No module named 'core'"
```bash
# Certifique-se de estar no diretório correto
cd requisitafacil-main
python manage.py gerar_dados_teste
```

### Problema: "Database is locked"
```bash
# Pare o servidor Django se estiver rodando
# Execute os testes novamente
python manage.py test core.tests.RequisicaoFacilTestCase
```

### Problema: "Permission denied"
```bash
# Verifique se o arquivo tem permissão de execução
chmod +x testar_sistema.py
python testar_sistema.py
```

### Problema: "Test failed"
```bash
# Limpe dados de teste antigos
python manage.py shell
>>> from core.models import Request, RequestItem, User
>>> RequestItem.objects.all().delete()
>>> Request.objects.all().delete()
>>> User.objects.filter(username__contains='teste').delete()
>>> exit()

# Execute os testes novamente
python manage.py test core.tests.RequisicaoFacilTestCase
```

## 📝 Logs de Teste

Os testes geram logs detalhados mostrando:

- ✅ Requisições criadas com sucesso
- ✅ KPIs calculados corretamente
- ✅ Fluxos completos funcionando
- ✅ Permissões validadas
- ✅ Estatísticas geradas

### Exemplo de Log
```
=== Testando criação de requisições falsas ===
✓ Requisição normal criada para FLV: F-1
✓ Requisição urgente criada para FLV: F-2
✓ Requisição aprovada criada para FLV: F-3
✓ Total de 27 requisições criadas com sucesso

=== Testando KPIs do gestor ===
✓ KPIs calculados corretamente:
  - Pendentes: 5
  - Aprovadas hoje: 4
  - Total do mês: 14
  - Departamentos ativos: 4
```

## 🎯 Próximos Passos

1. **Execute o script de teste**: `python testar_sistema.py`
2. **Escolha a opção 8** para executar tudo
3. **Verifique os logs** para confirmar que tudo funcionou
4. **Acesse o sistema** e verifique os KPIs manualmente
5. **Reporte qualquer problema** encontrado

## 📞 Suporte

Se encontrar problemas:

1. Verifique se o Django está configurado corretamente
2. Certifique-se de que o banco de dados está acessível
3. Verifique se todas as dependências estão instaladas
4. Execute `python manage.py check` para verificar configurações

---

**🎉 Sistema de testes criado com sucesso! Agora você pode verificar se todas as funcionalidades estão funcionando corretamente.** 