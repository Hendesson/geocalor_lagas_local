window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature) {
            var raw = feature.properties.NUM_PROTOC;
            var n = raw == null ? 0 : Number(raw);
            if (isNaN(n)) n = 0;
            var c = (n >= 19) ? '#00441b' :
                    (n >= 14) ? '#006d2c' :
                    (n >= 9)  ? '#238b45' :
                    (n >= 5)  ? '#41ab5d' :
                    (n >= 1)  ? '#e5f5e0' : '#e5f5e0';
            return { color: '#00441b', weight: 1, fillColor: c, fillOpacity: 0.7 };
        },
        function1: function(feature, layer) {
            if (!feature.properties) return;
            var p = feature.properties;
            var nome = p.NOME_PT != null ? p.NOME_PT : 'Sem nome';
            var num = p.NUM_PROTOC != null ? p.NUM_PROTOC : '-';
            layer.bindPopup('<strong>' + nome + '</strong><br>N\u00famero de protocolos: ' + num);
        },
        function2: function(feature) {
            return { fillColor: '#ffb347', color: '#333333', weight: 1.0, fillOpacity: 0.18 };
        },
        function3: function(feature) {
            var colors = { "1": "#6ec1a6", "2": "#e63946", "3": "#9b59b6", "4": "#2b9eb3", "5": "#ff9f1c" };
            var c = colors[String(feature.properties.codarea)] || "#cccccc";
            return { color: "#ffffff", weight: 1.5, fillColor: c, fillOpacity: 0.72 };
        },
        function4: function(feature, layer) {
            var info = {
                "1": { nome: "Norte", texto: "É difícil tratar a região norte como uma unidade, por conta do tamanho. Mas, no geral, as ondas de calor na região norte tendem a ser mais duradouras que no resto do Brasil — é bem comum encontrar ondas de calor que durem mais de 10 dias! As ondas de calor no Norte acontecem mais na primavera, que é o período de menor umidade. Além disso, as ondas de calor estão ficando mais frequentes na região Norte e em muitas partes estão ficando mais intensas e duradouras também. Em Manaus e Belém, por exemplo, a situação é bastante crítica!" },
                "2": { nome: "Nordeste", texto: "A região nordeste, como as temperaturas são naturalmente mais altas, as ondas de calor tendem a ser menos frequentes e mais curtas. No nordeste as ondas de calor são mais comuns no verão e são acompanhadas de umidade, ou seja, a tendência é de que fique quente durante a noite também." },
                "3": { nome: "Sudeste", texto: "A região sudeste no geral tem ondas de calor no verão e úmidas, mas nas partes mais longe do litoral, como Belo Horizonte, elas podem ocorrer também no fim do período de seca. As cidades da região sudeste não costumavam ter mais de 50 dias de ondas de calor por ano. Mas isso está se tornando mais comum nos anos recentes, em São Paulo e Belo Horizonte principalmente. Em BH, também identificamos que esses eventos estão ficando mais extremos." },
                "4": { nome: "Sul", texto: "A Região Sul também enfrenta os efeitos das mudanças climáticas, mas é a região brasileira menos afetada pelas ondas de calor. No geral, quando esses eventos acontecem, eles costumam ser nos meses de verão e não são muito duradouros, mas é até comum que as ondas de calor aconteçam próximas uma da outra, o que aumenta o desgaste acumulado na saúde." },
                "5": { nome: "Centro-Oeste", texto: "Na Região Centro-Oeste os meses de primavera costumam concentrar muito as ondas de calor e elas costumam acontecer nesse fim do período seco, quando a umidade começa a aumentar. Essa é uma região muito preocupante, pois as ondas de calor estão ficando cada vez mais frequentes, duradouras e intensas em todos os locais que analisamos." }
            };
            var d = info[String(feature.properties.codarea)];
            if (!d) return;
            layer.bindTooltip(
                '<div style="width:300px;font-family:sans-serif;line-height:1.6;white-space:normal;word-break:break-word">' +
                '<b style="font-size:13px;color:#1a2e44;display:block;margin-bottom:5px">' + d.nome + '</b>' +
                '<span style="font-size:11px;color:#5a6a7a">' + d.texto + '</span></div>',
                { sticky: true, opacity: 0.97 }
            );
        }
    }
});
