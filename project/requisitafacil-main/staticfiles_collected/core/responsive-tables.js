// Responsive Tables JavaScript
// Converte tabelas em cards em dispositivos móveis

document.addEventListener('DOMContentLoaded', function() {
    // Função para converter tabela em cards
    function convertTableToCards(table) {
        const tableWrapper = table.closest('.table-responsive-wrapper, .table-tabela, .table-responsive');
        if (!tableWrapper) return;

        // Verifica se já existe versão em cards
        if (tableWrapper.querySelector('.table-cards')) return;

        const thead = table.querySelector('thead');
        const tbody = table.querySelector('tbody');
        if (!thead || !tbody) return;

        // Obtém os cabeçalhos
        const headers = Array.from(thead.querySelectorAll('th')).map(th => th.textContent.trim());
        
        // Cria container para cards
        const cardsContainer = document.createElement('div');
        cardsContainer.className = 'table-cards';
        cardsContainer.style.display = 'none';

        // Converte cada linha em um card
        const rows = tbody.querySelectorAll('tr');
        rows.forEach((row, index) => {
            const card = document.createElement('div');
            card.className = 'table-card';
            
            const cells = row.querySelectorAll('td');
            let cardHTML = '';
            
            cells.forEach((cell, cellIndex) => {
                if (headers[cellIndex]) {
                    cardHTML += `
                        <div class="table-card-item">
                            <div class="table-card-header">${headers[cellIndex]}</div>
                            <div class="table-card-value">${cell.innerHTML}</div>
                        </div>
                    `;
                }
            });
            
            card.innerHTML = cardHTML;
            cardsContainer.appendChild(card);
        });

        // Adiciona os cards ao wrapper
        tableWrapper.appendChild(cardsContainer);
    }

    // Função para mostrar/ocultar versão apropriada baseada no tamanho da tela
    function toggleTableResponsive() {
        const tables = document.querySelectorAll('.table');
        const isMobile = window.innerWidth <= 768;
        
        tables.forEach(table => {
            const wrapper = table.closest('.table-responsive-wrapper, .table-tabela, .table-responsive');
            if (!wrapper) return;

            const cardsContainer = wrapper.querySelector('.table-cards');
            
            if (isMobile) {
                // Em mobile, esconde tabela e mostra cards
                table.style.display = 'none';
                if (cardsContainer) {
                    cardsContainer.style.display = 'block';
                } else {
                    // Se não existem cards, cria eles
                    convertTableToCards(table);
                    setTimeout(() => {
                        const newCardsContainer = wrapper.querySelector('.table-cards');
                        if (newCardsContainer) {
                            newCardsContainer.style.display = 'block';
                        }
                    }, 100);
                }
            } else {
                // Em desktop, mostra tabela e esconde cards
                table.style.display = 'table';
                if (cardsContainer) {
                    cardsContainer.style.display = 'none';
                }
            }
        });
    }

    // Converte todas as tabelas na página
    const tables = document.querySelectorAll('.table');
    tables.forEach(convertTableToCards);

    // Executa na carga inicial
    toggleTableResponsive();

    // Executa quando a janela é redimensionada
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(toggleTableResponsive, 250);
    });

    // Função para melhorar a experiência em dispositivos móveis
    function enhanceMobileExperience() {
        if (window.innerWidth <= 768) {
            // Adiciona classes para melhor espaçamento em mobile
            const cards = document.querySelectorAll('.table-card');
            cards.forEach(card => {
                card.style.marginBottom = '15px';
                card.style.padding = '15px';
            });

            // Melhora botões em mobile
            const buttons = document.querySelectorAll('.table-card .btn');
            buttons.forEach(btn => {
                btn.style.margin = '5px 5px 5px 0';
                btn.style.fontSize = '0.8rem';
            });
        }
    }

    // Executa melhorias mobile
    enhanceMobileExperience();

    // Observa mudanças no DOM para novas tabelas
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    const tables = node.querySelectorAll ? node.querySelectorAll('.table') : [];
                    if (node.classList && node.classList.contains('table')) {
                        tables.push(node);
                    }
                    tables.forEach(convertTableToCards);
                }
            });
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// Função utilitária para adicionar classes responsivas
function addResponsiveClasses() {
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        // Adiciona classes para colunas menos importantes
        const cells = table.querySelectorAll('td, th');
        cells.forEach((cell, index) => {
            // Esconde colunas menos importantes em mobile
            if (index >= 4) { // A partir da 5ª coluna
                cell.classList.add('hide-mobile');
            }
        });
    });
}

// Executa quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addResponsiveClasses);
} else {
    addResponsiveClasses();
} 