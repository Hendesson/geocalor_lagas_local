document.addEventListener("DOMContentLoaded", function () {
    var HIDDEN_PATHS = ['/', '/inicio', '/contato'];

    var btn = document.createElement("button");
    btn.innerHTML = '<i class="fas fa-print" style="margin-right:8px"></i>Baixar PDF';
    btn.className = "btn btn-primary shadow print-hide";
    btn.style.cssText = [
        "position:fixed", "bottom:24px", "right:24px", "z-index:9999",
        "border-radius:50px", "padding:10px 20px", "font-weight:600",
        "box-shadow:0 4px 12px rgba(0,0,0,0.25)", "cursor:pointer",
    ].join(";");
    btn.onclick = function () { window.print(); };
    document.body.appendChild(btn);

    function updateVisibility() {
        var path = window.location.pathname.replace(/\/$/, '') || '/';
        btn.style.display = HIDDEN_PATHS.indexOf(path) !== -1 ? 'none' : '';
    }

    updateVisibility();

    var _push = history.pushState;
    history.pushState = function () {
        _push.apply(history, arguments);
        updateVisibility();
    };
    window.addEventListener('popstate', updateVisibility);
});
