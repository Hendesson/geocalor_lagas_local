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
        }
    }
});
