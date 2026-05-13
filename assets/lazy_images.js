// Aplica loading="lazy" em imagens abaixo da dobra.
// Dash 3.x não aceita o atributo via prop — aplicamos via JS após o DOM estar pronto.
// Imagens acima da dobra (logo do banner, ícone do navbar) são excluídas por classe.
(function () {
    var EAGER_CLASSES = ['navbar-brand', 'inicio-brand-logo'];

    function applyLazy() {
        var imgs = document.querySelectorAll('img:not([loading])');
        imgs.forEach(function (img) {
            var skip = EAGER_CLASSES.some(function (cls) {
                return img.closest('.' + cls);
            });
            if (!skip) img.setAttribute('loading', 'lazy');
        });
    }

    // Primeira passagem após carregamento inicial
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyLazy);
    } else {
        applyLazy();
    }

    // Re-aplica após cada navegação SPA (Dash troca o conteúdo via React)
    var _push = history.pushState;
    history.pushState = function () {
        _push.apply(history, arguments);
        setTimeout(applyLazy, 300);
    };
    window.addEventListener('popstate', function () {
        setTimeout(applyLazy, 300);
    });
})();
