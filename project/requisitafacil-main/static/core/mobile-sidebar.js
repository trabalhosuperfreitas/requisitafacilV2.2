// Mobile Sidebar JavaScript
// Controla o sidebar responsivo em dispositivos móveis

document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    
    // Função para abrir o sidebar
    function openSidebar() {
        sidebar.classList.add('show');
        sidebarOverlay.classList.add('show');
        mobileMenuToggle.classList.add('active');
        document.body.style.overflow = 'hidden'; // Previne scroll do body
    }
    
    // Função para fechar o sidebar
    function closeSidebar() {
        sidebar.classList.remove('show');
        sidebarOverlay.classList.remove('show');
        mobileMenuToggle.classList.remove('active');
        document.body.style.overflow = ''; // Restaura scroll do body
    }
    
    // Event listener para o botão hambúrguer
    mobileMenuToggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        if (sidebar.classList.contains('show')) {
            closeSidebar();
        } else {
            openSidebar();
        }
    });
    
    // Event listener para o overlay (fechar ao clicar fora)
    sidebarOverlay.addEventListener('click', function() {
        closeSidebar();
    });
    
    // Event listener para tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    });
    
    // Fechar sidebar ao clicar em links do menu (em mobile)
    const menuLinks = sidebar.querySelectorAll('.menu-link');
    menuLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Só fecha se estiver em mobile
            if (window.innerWidth <= 768) {
                setTimeout(closeSidebar, 100); // Pequeno delay para feedback visual
            }
        });
    });
    
    // Função para verificar se está em mobile
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    // Melhorias de acessibilidade
    mobileMenuToggle.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            mobileMenuToggle.click();
        }
    });
    
    // Foco management para acessibilidade
    function trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
        );
        
        const firstFocusableElement = focusableElements[0];
        const lastFocusableElement = focusableElements[focusableElements.length - 1];
        
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstFocusableElement) {
                        e.preventDefault();
                        lastFocusableElement.focus();
                    }
                } else {
                    if (document.activeElement === lastFocusableElement) {
                        e.preventDefault();
                        firstFocusableElement.focus();
                    }
                }
            }
        });
    }
    
    // Aplica trap focus quando o sidebar está aberto
    function setupFocusTrap() {
        if (sidebar.classList.contains('show')) {
            trapFocus(sidebar);
        }
    }
    
    // Observa mudanças no sidebar para aplicar focus trap
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                if (sidebar.classList.contains('show')) {
                    setupFocusTrap();
                }
            }
        });
    });
    
    observer.observe(sidebar, {
        attributes: true,
        attributeFilter: ['class']
    });
    
    // Melhorias de performance
    let isScrolling = false;
    
    window.addEventListener('scroll', function() {
        if (!isScrolling) {
            isScrolling = true;
            requestAnimationFrame(function() {
                // Lógica de scroll se necessário
                isScrolling = false;
            });
        }
    });
    
    // Previne scroll do body quando sidebar está aberto
    function preventBodyScroll() {
        if (sidebar.classList.contains('show')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
    
    // Observa mudanças para prevenir scroll
    const bodyObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                preventBodyScroll();
            }
        });
    });
    
    bodyObserver.observe(sidebar, {
        attributes: true,
        attributeFilter: ['class']
    });
});

// Função utilitária para verificar se o dispositivo é touch
function isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

// Melhorias para dispositivos touch
if (isTouchDevice()) {
    document.addEventListener('DOMContentLoaded', function() {
        const sidebar = document.getElementById('sidebar');
        
        // Adiciona suporte a swipe para fechar
        let startX = 0;
        let currentX = 0;
        
        sidebar.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
        });
        
        sidebar.addEventListener('touchmove', function(e) {
            currentX = e.touches[0].clientX;
        });
        
        sidebar.addEventListener('touchend', function(e) {
            const diffX = startX - currentX;
            
            // Se o usuário fez swipe para a esquerda (fechar)
            if (diffX > 50 && sidebar.classList.contains('show')) {
                document.getElementById('mobile-menu-toggle').click();
            }
        });
    });
} 