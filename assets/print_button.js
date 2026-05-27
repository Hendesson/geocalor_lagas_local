document.addEventListener("DOMContentLoaded", function () {
    var HIDDEN_PATHS = ['/', '/inicio', '/contato'];

    var H2C_URL   = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
    var JSPDF_URL = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';

    var PAGE_NAMES = {
        'temperaturas':    'GeoCalor_Caracterizacao_Climatica',
        'ondas':           'GeoCalor_Ondas_de_Calor',
        'sih-sim':         'GeoCalor_Perfil_Epidemiologico',
        'mortalidade':     'GeoCalor_Mortalidade_OC',
        'correlacao':      'GeoCalor_Internacao_OC',
        'sistemas-alerta': 'GeoCalor_Sistemas_de_Alerta',
    };

    var BG = '#f0f7fb';

    function pdfFilename() {
        var slug = window.location.pathname.replace(/^\//, '').replace(/\/$/, '') || 'dashboard';
        return (PAGE_NAMES[slug] || 'GeoCalor_Dashboard') + '.pdf';
    }

    var btn = document.createElement('button');
    btn.innerHTML = '<i class="fas fa-file-pdf" style="margin-right:8px"></i>Baixar PDF';
    btn.className = 'btn btn-primary shadow print-hide';
    btn.style.cssText = [
        'position:fixed', 'bottom:24px', 'right:24px', 'z-index:9999',
        'border-radius:50px', 'padding:10px 20px', 'font-weight:600',
        'box-shadow:0 4px 12px rgba(0,0,0,0.25)', 'cursor:pointer',
    ].join(';');

    function loadScript(src, cb) {
        if (document.querySelector('script[src="' + src + '"]')) { cb(); return; }
        var s = document.createElement('script');
        s.src = src;
        s.onload = cb;
        s.onerror = function () {
            alert('Não foi possível carregar biblioteca de PDF.\nVerifique a conexão com a internet.');
            restoreBtn();
        };
        document.head.appendChild(s);
    }

    var labelOrig = btn.innerHTML;

    function restoreBtn() {
        btn.innerHTML = labelOrig;
        btn.disabled = false;
    }

    btn.onclick = function () {
        labelOrig = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right:8px"></i>Carregando...';
        btn.disabled = true;
        loadScript(H2C_URL, function () {
            loadScript(JSPDF_URL, runCapture);
        });
    };

    function runCapture() {
        var content = document.getElementById('page-content');
        if (!content) { restoreBtn(); return; }

        btn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right:8px"></i>Capturando...';

        var hidden = [];
        content.querySelectorAll('.modebar, .btn-download-asset, .sihsim-section-banner').forEach(function (el) {
            hidden.push({ el: el, vis: el.style.visibility });
            el.style.visibility = 'hidden';
        });

        html2canvas(content, {
            scale: 2,
            useCORS: true,
            allowTaint: true,
            logging: false,
            backgroundColor: BG,
            windowWidth: Math.max(content.scrollWidth, 1280),
        }).then(function (canvas) {
            hidden.forEach(function (item) { item.el.style.visibility = item.vis; });

            btn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right:8px"></i>Gerando PDF...';

            var jsPDF   = (window.jspdf && window.jspdf.jsPDF) || window.jsPDF;
            var pdf     = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4', compress: true });
            var pageW   = pdf.internal.pageSize.getWidth();
            var pageH   = pdf.internal.pageSize.getHeight();
            var pxPerMm = canvas.width / pageW;
            var pageHpx = Math.floor(pageH * pxPerMm);
            var totalH  = canvas.height;
            var yPx     = 0;
            var page    = 0;

            while (yPx < totalH) {
                if (page > 0) pdf.addPage();

                var sliceH  = Math.min(pageHpx, totalH - yPx);
                var slice   = document.createElement('canvas');
                slice.width  = canvas.width;
                slice.height = sliceH;
                var ctx = slice.getContext('2d');
                ctx.fillStyle = BG;
                ctx.fillRect(0, 0, slice.width, slice.height);
                ctx.drawImage(canvas, 0, yPx, canvas.width, sliceH, 0, 0, canvas.width, sliceH);

                pdf.addImage(
                    slice.toDataURL('image/jpeg', 0.92),
                    'JPEG', 0, 0,
                    pageW, sliceH / pxPerMm
                );

                yPx += pageHpx;
                page++;
            }

            pdf.save(pdfFilename());
            restoreBtn();
        }).catch(function (err) {
            hidden.forEach(function (item) { item.el.style.visibility = item.vis; });
            console.error('[GeoCalor PDF]', err);
            alert('Erro ao capturar página:\n' + err.message);
            restoreBtn();
        });
    }

    document.body.appendChild(btn);

    function updateVisibility() {
        var path = window.location.pathname.replace(/\/$/, '') || '/';
        btn.style.display = HIDDEN_PATHS.indexOf(path) !== -1 ? 'none' : '';
    }

    updateVisibility();
    var _push = history.pushState;
    history.pushState = function () { _push.apply(history, arguments); updateVisibility(); };
    window.addEventListener('popstate', updateVisibility);
});
