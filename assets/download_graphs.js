/* Download de gráficos Plotly via evento delegado.
 * data-plotly-download="<graph-id>"  → download PNG de um gráfico individual.
 * data-mapa-download="<container-id>" → download PNG de mapa(s) coropléticos:
 *   - ano único : download direto do mapa
 *   - todos os anos : combina todos em grid 3 colunas e baixa uma imagem única */

document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-plotly-download]');
    if (!btn) return;
    var graphId  = btn.getAttribute('data-plotly-download');
    var filename = btn.getAttribute('data-plotly-filename') || graphId;
    var wrapper  = document.getElementById(graphId);
    var graphDiv = wrapper && (wrapper.querySelector('.js-plotly-plot') || wrapper);
    if (graphDiv && window.Plotly) {
        Plotly.downloadImage(graphDiv, {
            format:   'png',
            filename: filename,
            width:    1400,
            height:   800,
            scale:    2,
        });
    }
}, false);

document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-mapa-download]');
    if (!btn) return;

    var containerId = btn.getAttribute('data-mapa-download');
    var filename    = btn.getAttribute('data-mapa-filename') || 'mapa';
    var container   = document.getElementById(containerId);
    if (!container || !window.Plotly) return;

    var plots = Array.from(container.querySelectorAll('.js-plotly-plot'));
    if (plots.length === 0) return;

    /* ── Ano único ──────────────────────────────────────────────────────── */
    if (plots.length === 1) {
        Plotly.downloadImage(plots[0], {
            format: 'png', filename: filename, width: 1200, height: 700, scale: 2,
        });
        return;
    }

    /* ── Todos os anos: combina em grid 3 colunas (sequencial para evitar artefatos) ── */
    var COLS = 3;
    var W = 600, H = 380;
    var rows   = Math.ceil(plots.length / COLS);
    var canvas = document.createElement('canvas');
    canvas.width  = COLS * W;
    canvas.height = rows  * H;
    var ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    var titles = Array.from(container.querySelectorAll('h6')).map(function (h) {
        return h.textContent.trim();
    });

    (async function () {
        for (var i = 0; i < plots.length; i++) {
            var dataUrl = await Plotly.toImage(plots[i], { format: 'png', width: W, height: H, scale: 1 });
            await new Promise(function (resolve) {
                var img = new Image();
                img.onload = function () {
                    var col = i % COLS;
                    var row = Math.floor(i / COLS);
                    ctx.drawImage(img, col * W, row * H, W, H);
                    /* Label do ano sobreposto no canto superior esquerdo da célula */
                    if (titles[i]) {
                        ctx.fillStyle = 'rgba(255,255,255,0.82)';
                        ctx.fillRect(col * W + 4, row * H + 4, 58, 22);
                        ctx.fillStyle = '#1761a0';
                        ctx.font = 'bold 13px Segoe UI, Arial, sans-serif';
                        ctx.fillText(titles[i], col * W + 8, row * H + 20);
                    }
                    resolve();
                };
                img.src = dataUrl;
            });
        }
        var a = document.createElement('a');
        a.href     = canvas.toDataURL('image/png');
        a.download = filename + '_todos_anos.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    })();
}, false);
