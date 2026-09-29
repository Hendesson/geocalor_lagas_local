"""HTML estático das notas técnicas (impressão/PDF) — mesmo conteúdo dos dashboards separados."""

NOTA_SISTEMAS_ALERTA_LINKS = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sistemas de Alerta — Links e Documentos de Referência</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 1000px;
           margin: 40px auto; padding: 0 2rem; color: #222; line-height: 1.7; }
    h1 { color: #1761a0; border-bottom: 3px solid #6ec1a6; padding-bottom: 8px; }
    h2 { color: #1761a0; margin-top: 2rem; font-size: 1.15rem; }
    p  { margin: 0.5rem 0; }
    table { border-collapse: collapse; width: 100%; margin: 1.5rem 0; font-size: 0.92rem; }
    th { background: #1761a0; color: #fff; padding: 10px 14px; text-align: left; }
    td { border: 1px solid #dee2e6; padding: 9px 13px; vertical-align: top; }
    tr:nth-child(even) td { background: #f0f7fb; }
    tr:hover td { background: #ddeef8; }
    .pais { font-weight: 700; color: #1761a0; white-space: nowrap; }
    .links-cell a { display: block; color: #1761a0; text-decoration: none;
                    margin-bottom: 4px; word-break: break-all; }
    .links-cell a:hover { text-decoration: underline; color: #2b9eb3; }
    .links-cell a::before { content: "→ "; font-size: 0.85em; }
    .badge { display: inline-block; background: #e8f4fb; color: #1761a0;
             border-radius: 4px; padding: 1px 7px; font-size: 0.78rem;
             font-weight: 600; margin-right: 4px; white-space: nowrap; }
    .intro { background: #f0f7fb; border-left: 4px solid #2b9eb3;
             padding: 12px 16px; border-radius: 4px; margin-bottom: 1.5rem; }
    .no-print-btn { text-align: right; margin-bottom: 1rem; }
    .no-print-btn button { background: #1761a0; color: #fff; border: none;
                           padding: 8px 18px; border-radius: 6px; cursor: pointer;
                           font-size: 0.9rem; }
    .no-print-btn button:hover { background: #2b9eb3; }
    @media print {
      .no-print-btn { display: none; }
      a::after { content: none !important; }
      tr:hover td { background: inherit; }
    }
  </style>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LHX5DN0BCW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-LHX5DN0BCW', {page_title: document.title + ' | GeoCalor'});
  </script>
</head>
<body>

  <div style="display:flex;align-items:center;gap:20px;margin:16px 0 24px;flex-wrap:wrap;">
    <img src="/assets/sistemas_alerta/images/lagasLogo.png" alt="LAGAS"
         style="max-height:64px;max-width:130px;object-fit:contain;">
    <img src="/assets/sistemas_alerta/images/geocalorLogo.png" alt="GeoCalor"
         style="max-height:64px;max-width:130px;object-fit:contain;">
    <img src="/assets/unb.png" alt="UnB"
         style="max-height:64px;max-width:130px;object-fit:contain;">
    <img src="/assets/fiocruz.png" alt="Fiocruz"
         style="max-height:64px;max-width:130px;object-fit:contain;">
    <img src="/assets/ufrj_logo.png" alt="UFRJ"
         style="max-height:64px;max-width:130px;object-fit:contain;">
    <img src="/assets/lmi_logo.png" alt="LMI-Sentinela"
         style="max-height:64px;max-width:130px;object-fit:contain;">
  </div>

  <div class="no-print-btn">
    <button onclick="window.print()">Imprimir / Salvar como PDF</button>
  </div>

  <h1>Sistemas de Alerta — Links e Documentos de Referência</h1>
  <p><em>Projeto GeoCalor | LAGAS / UnB, Fiocruz/OCS, LASA-UFRJ &amp; LMI-Sentinela</em></p>

  <div class="intro">
    <p>Levantamento de políticas nacionais e planos de ação relacionados à adaptação ao
    calor extremo e sistemas de alerta ao redor do mundo. Os documentos foram identificados
    e analisados como parte da revisão de sistemas internacionais de alerta conduzida pelo
    Projeto GeoCalor. Ao total, foram identificados 63 documentos, oriundos de 18 países.</p>
  </div>

  <table>
    <thead>
      <tr>
        <th style="width:12%">País</th>
        <th style="width:38%">Políticas adotadas</th>
        <th style="width:50%">Links para consulta</th>
      </tr>
    </thead>
    <tbody>

      <tr>
        <td class="pais">Austrália</td>
        <td>Estratégia nacional de adaptação às mudanças climáticas
            <span class="badge">National Adaptation Plan</span></td>
        <td class="links-cell">
          <a href="https://www.dcceew.gov.au/climate-change/policy/adaptation/nap" target="_blank" rel="noopener">Plano Nacional de Adaptação</a>
          <a href="https://www.agriculture.gov.au/sites/default/files/documents/national-climate-resilience-and-adaptation-strategy.pdf" target="_blank" rel="noopener">National Climate Resilience and Adaptation Strategy (PDF)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Áustria</td>
        <td>Adaptação ao calor extremo como parte da política nacional de saúde e clima.
            <span class="badge">National Adaptation Plan 2024</span></td>
        <td class="links-cell">
          <a href="https://unfccc.int/documents/645549" target="_blank" rel="noopener">Plano Nacional (UNFCCC)</a>
          <a href="https://www.bmluk.gv.at/en/topics/climate-environment/climate/adaptation-to-climate-change/austrian-strategy-adaptaion.html" target="_blank" rel="noopener">Site oficial do governo austríaco</a>
          <a href="https://climate-adapt.eea.europa.eu/en/metadata/publications/national-adaptation-strategy-austria" target="_blank" rel="noopener">Publicações relacionadas — Climate-ADAPT</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Bangladesh</td>
        <td>Desenvolvimento incipiente de uma estratégia nacional de adaptação às mudanças climáticas.
            <span class="badge">National Adaptation Plan 2023–2050</span></td>
        <td class="links-cell">
          <a href="https://moef.portal.gov.bd/sites/default/files/files/moef.portal.gov.bd/npfblock/903c6d55_3fa3_4d24_a4e1_0611eaa3cb69/National%20Adaptation%20Plan%20of%20Bangladesh%20%282023-2050%29%20%281%29.pdf" target="_blank" rel="noopener">Plano Nacional de Adaptação (PDF)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Bélgica</td>
        <td>Adaptação ao calor extremo como parte da política nacional de saúde e clima.
            <span class="badge">National Adaptation Plan / Climate law 2017–2020</span></td>
        <td class="links-cell">
          <a href="https://www.cnc-nkc.be/sites/default/files/report/file/nap_en.pdf" target="_blank" rel="noopener">Plano Nacional de Adaptação (PDF)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Brasil</td>
        <td>Planos locais. Lançamento em 2025 do Belém Health Action Plan no âmbito da COP30,
            que aborda o tema de calor extremo.
            <span class="badge">Plano Clima 2024–2035</span>
            <span class="badge">Estratégia Nacional de Mitigação</span></td>
        <td class="links-cell">
          <a href="https://cdn.who.int/media/docs/default-source/climate-change/en---belem-action-plan.pdf" target="_blank" rel="noopener">Belém Health Action Plan (PDF)</a>
          <a href="https://www.gov.br/mma/pt-br/composicao/smc/plano-clima/apresentacao-plano-clima-atualizada-mai24-lgc-1.pdf" target="_blank" rel="noopener">Plano Clima 2024–2035 (PDF)</a>
          <a href="https://www.gov.br/mma/pt-br/composicao/smc/plano-clima/plano-clima-mitigacao" target="_blank" rel="noopener">Estratégia Nacional de Mitigação</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Canadá</td>
        <td>Estratégias das províncias de adaptação às mudanças climáticas. Estratégia nacional
            lançada em 2023, depois das iniciativas das províncias.</td>
        <td class="links-cell">
          <a href="https://unfccc.int/sites/default/files/resource/NAP-Canada-2024-EN.pdf" target="_blank" rel="noopener">Estratégia Nacional de Adaptação (PDF)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Espanha</td>
        <td>Estratégia nacional de mudanças climáticas.
            <span class="badge">PNACC 2021–2030</span></td>
        <td class="links-cell">
          <a href="https://www.miteco.gob.es/es/cambio-climatico/temas/impactos-vulnerabilidad-y-adaptacion/plan-nacional-adaptacion-cambio-climatico.html" target="_blank" rel="noopener">Plan Nacional de Adaptación al Cambio Climático</a>
        </td>
      </tr>

      <tr>
        <td class="pais">EUA</td>
        <td>Agências como FEMA, NOAA e CDC promovem planos de alerta. Cada governo estadual e local
            tem autonomia para criar o seu. Recente adoção de uma estratégia nacional de adaptação.</td>
        <td class="links-cell">
          <a href="https://2021-2025.state.gov/office-of-the-spokesperson/releases/2025/01/u-s-national-adaptation-and-resilience-planning-strategy/" target="_blank" rel="noopener">National Adaptation and Resilience Planning Strategy</a>
        </td>
      </tr>

      <tr>
        <td class="pais">França</td>
        <td>Integração do risco por calor extremo em políticas nacionais de clima e saúde.
            <span class="badge">Stratégie nationale d'adaptation</span></td>
        <td class="links-cell">
          <a href="https://www.ecologie.gouv.fr/sites/default/files/documents/ONERC_Rapport_2006_Strategie_Nationale_WEB.pdf" target="_blank" rel="noopener">Stratégie nationale d'adaptation au changement climatique (PDF)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Índia</td>
        <td>Governo nacional e estaduais promovem diretrizes e planos específicos de atuação.
            <span class="badge">Heat Action Plans</span>
            Liderança da NDMA (National Disaster Management Authority).</td>
        <td class="links-cell">
          <a href="https://ncdc.mohfw.gov.in/wp-content/uploads/2024/05/3-PPT-Heat-wave-Management-Preparedness-and-response-NDMA.pdf" target="_blank" rel="noopener">Diretrizes da NDMA — Gestão de Ondas de Calor (PDF)</a>
          <a href="https://www.ndma.gov.pk/storage/publications/July2024/oxTpPKvfpQjxCZTrLiuv.pdf" target="_blank" rel="noopener">Heatwave Guidelines (PDF)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Luxemburgo</td>
        <td>Adaptação ao calor extremo como parte da política nacional de saúde e clima.
            <span class="badge">National Adaptation Plan 2018–2023</span></td>
        <td class="links-cell">
          <a href="https://climate-laws.org/document/strategy-and-action-plan-for-adaptation-to-climate-change-in-luxembourg-2018-2023_a1f0" target="_blank" rel="noopener">Strategy and Action Plan for Adaptation to Climate Change</a>
          <a href="https://www.zesumme-vereinfachen.lu/en-GB/projects/klimaadaptatiounsstrategie" target="_blank" rel="noopener">Consulta pública para atualização 2024–2025</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Macedônia</td>
        <td><span class="badge">National Adaptation Plan 2024–2027</span>
            Projeto aprovado em 2024 com suporte da UNDP.</td>
        <td class="links-cell">
          <a href="https://www.adaptation-undp.org/projects/improving-resilience-republic-north-macedonia-integrating-adaptation-planning-processes" target="_blank" rel="noopener">Improving Resilience — Republic of North Macedonia (UNDP)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Paquistão</td>
        <td>Adaptação às mudanças climáticas. Ministério de Mudanças Climáticas estrutura as
            políticas setoriais correspondentes.
            <span class="badge">National Adaptation Plan 2023</span></td>
        <td class="links-cell">
          <a href="https://heathealth.info/resources/pakistan-heatwave-guidelines-2024/" target="_blank" rel="noopener">Heatwave Guidelines 2024</a>
          <a href="https://unfccc.int/sites/default/files/resource/National_Adaptation_Plan_Pakistan.pdf" target="_blank" rel="noopener">National Adaptation Plan — Paquistão (PDF)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Portugal</td>
        <td>Planos sazonais de contingência (verão — módulo calor) e planos específicos de
            contingência no nível nacional. Realizados pela Direção Geral de Saúde.</td>
        <td class="links-cell">
          <a href="https://www.dgs.pt/em-destaque/plano-para-a-resposta-sazonal-em-saude-referencial-tecnico-modulo-verao-2025-pdf.aspx" target="_blank" rel="noopener">Plano Sazonal de Resposta em Saúde — Módulo Verão 2025</a>
          <a href="https://climate-adapt.eea.europa.eu/pt/metadata/case-studies/operation-of-the-portuguese-contingency-heatwaves-plan" target="_blank" rel="noopener">Análise do Plano de Contingência — Climate-ADAPT</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Reino Unido</td>
        <td>Estratégia nacional intersetorial de adaptação ao calor extremo com ferramentas
            para adaptação local.
            <span class="badge">National Adaptation Programme</span></td>
        <td class="links-cell">
          <a href="https://www.gov.uk/government/publications/third-national-adaptation-programme-nap3" target="_blank" rel="noopener">Third National Adaptation Programme (NAP3)</a>
          <a href="https://www.gov.uk/government/publications/beat-the-heat-hot-weather-advice/beat-the-heat-staying-safe-in-hot-weather" target="_blank" rel="noopener">Beat the Heat — Hot Weather Advice</a>
          <a href="https://lcat.uk/" target="_blank" rel="noopener">Local Climate Adaptation Tool (LCAT)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Santa Lúcia</td>
        <td>Estratégia geral de adaptação climática, pela condição insular da nação.
            <span class="badge">National Adaptation Plan 2018–2028</span></td>
        <td class="links-cell">
          <a href="https://unfccc.int/sites/default/files/resource/NAP-Saint-Lucia-2018.pdf" target="_blank" rel="noopener">National Adaptation Plan — Santa Lúcia (PDF)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Síria</td>
        <td>Plano desenvolvido por uma ONG em parceria com a UNDP. Não há políticas setoriais
            do tema no governo.</td>
        <td class="links-cell">
          <a href="https://www.adaptation-undp.org/explore/arab-states/syrian-arab-republic" target="_blank" rel="noopener">Syrian Arab Republic — Adaptation (UNDP)</a>
        </td>
      </tr>

      <tr>
        <td class="pais">Suíça</td>
        <td>Adaptação ao calor extremo como parte da política nacional de saúde e clima.
            Diretrizes do governo federal contidas no Action Plan 2020–2025.
            <span class="badge">National Adaptation Plan (em revisão)</span></td>
        <td class="links-cell">
          <a href="https://www.nccs.admin.ch/nccs/en/home/climate-change-and-impacts/analyse-der-klimabedingten-risiken-und-chancen.html" target="_blank" rel="noopener">National Center for Climate Services (NCCS)</a>
          <a href="https://www.bafu.admin.ch/en/climate-strategy-adaptation" target="_blank" rel="noopener">Action Plan 2020–2025</a>
          <a href="https://www.bafu.admin.ch/en/publication?id=RZ7HTchQoLVu" target="_blank" rel="noopener">First Adaptation Plan 2012</a>
        </td>
      </tr>

    </tbody>
  </table>

  <p style="margin-top:2rem;font-size:0.85rem;color:#666;">
    <em>Fonte: levantamento realizado pelo Projeto GeoCalor — LAGAS/UnB, Fiocruz/OCS,
    LASA-UFRJ &amp; LMI-Sentinela. Dados coletados até 2025.</em>
  </p>

  <p class="no-print-btn" style="text-align:right;margin-top:1.5rem;">
    <button onclick="window.print()">Imprimir / Salvar como PDF</button>
  </p>

</body>
</html>"""

NOTA_MORTALIDADE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Nota Técnica — Excesso de Mortalidade em Ondas de Calor</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px;
           margin: 40px auto; padding: 0 2rem; color: #222; line-height: 1.7; }
    h1 { color: #1761a0; border-bottom: 3px solid #6ec1a6; padding-bottom: 8px; }
    h2 { color: #1761a0; margin-top: 2rem; font-size: 1.2rem; }
    code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-size: 0.95em; }
    .formula { background: #f8f9fa; border-left: 4px solid #6ec1a6;
               padding: 12px 16px; margin: 12px 0; border-radius: 4px; font-family: monospace; font-size: 0.95em; }
    table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
    th, td { border: 1px solid #dee2e6; padding: 8px 12px; text-align: left; }
    th { background: #e8f4fb; color: #1761a0; }
    .sig { color: #e63946; font-weight: bold; }
    .prot { color: #1761a0; font-weight: bold; }
    @media print {
      a[href]::after { content: none !important; }
      .no-print { display: none; }
    }
  </style>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LHX5DN0BCW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-LHX5DN0BCW', {page_title: document.title + ' | GeoCalor'});
  </script>
</head>
<body>
  <div style="display:flex;align-items:center;gap:24px;margin:16px 0 24px;flex-wrap:wrap;">
    <img src="/assets/sistemas_alerta/images/lagasLogo.png" alt="LAGAS"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/sistemas_alerta/images/geocalorLogo.png" alt="GeoCalor"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/unb.png" alt="UnB"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/fiocruz.png" alt="Fiocruz"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/ufrj_logo.png" alt="UFRJ"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/lmi_logo.png" alt="LMI-Sentinela"
         style="max-height:70px;max-width:140px;object-fit:contain;">
  </div>

  <h1>Nota Técnica — Excesso de Mortalidade em Ondas de Calor e Fatores de Risco</h1>
  <p><em>Projeto GeoCalor | LAGAS / UnB, Fiocruz/OCS, LASA-UFRJ &amp; LMI-Sentinela</em></p>

  <h2>1. Definição do excesso de mortalidade para cada onda de calor</h2>

  <p>O excesso de mortalidade foi identificado para cada evento individual através da razão
  entre mortalidade observada e esperada (O/E Ratio). O cálculo foi feito de acordo com
  a fórmula abaixo.</p>

  <div class="formula">
    (O/E)<sub>ij</sub> = M<sub>ij</sub> / ((M<sub>i1</sub> + M<sub>i2</sub> + … +
    M<sub>i,j−1</sub> + M<sub>i,j+1</sub> + … + M<sub>ik−1</sub> + M<sub>ik</sub>) / (k−1))
  </div>

  <p>Onde M<sub>ij</sub> é a mortalidade total da i-ésima onda de calor do ano j e k é o
  total de anos na série histórica. Ou seja, a mortalidade total de uma onda é dividida
  pela média da mortalidade do mesmo período do ano em todos os demais anos,
  excluindo-se anos que também houve onda de calor no mesmo período.</p>

  <p><strong>Exemplo:</strong> uma onda de calor que aconteceu entre 10 e 13 de janeiro
  de 2010. A mortalidade total desses dias será dividida pela média da mortalidade desses
  mesmos dias em cada ano entre 2011 e 2023.</p>

  <p>Ao final foi calculado o intervalo de confiança de 95% para identificação das ondas
  em que a razão foi significativa, tanto para excesso de mortalidade, como para
  diminuição de mortalidade.</p>

  <h2>2. Identificação dos fatores de risco para ocorrência de excesso de mortalidade</h2>

  <p>Para cada onda de calor foram levantados alguns indicadores climáticos, são esses:
  a duração da onda, a amplitude térmica média da onda, a umidade média da onda,
  a anomalia de temperatura média da onda, a distância em dias para a última onda de
  calor e o valor médio do EHF da onda.</p>

  <p>A partir desses indicadores foram utilizadas as medianas dos valores de todas as
  ondas em cada região metropolitana para definir valores altos (acima da mediana) e
  baixos (abaixo da mediana). A partir dessa classificação foram construídas tabelas de
  contingência (2×2) e calculadas as razões de prevalência e os respectivos intervalos
  de confiança para definir em cada região metropolitana quais características climáticas
  estão mais associadas a ondas de calor com excesso de mortalidade.</p>

  <p><strong>Exemplo:</strong> Uma razão de prevalência significativa de 1,50 para o
  indicador "duração alta", indica que nessa região metropolitana, ondas de calor com
  alta duração (acima da mediana) têm prevalência 50% maior de excesso de mortalidade,
  portanto a alta duração é um fator de risco para excesso de mortalidade.</p>

  <p>Por outro lado, uma razão de prevalência significativa de 0,5 para o indicador
  "umidade alta" indica que as ondas de calor de alta umidade têm prevalência 50%
  menor de excesso de mortalidade, portanto a alta umidade é um fator protetor para
  o excesso de mortalidade, enquanto a umidade baixa é um fator de risco.</p>

  <p class="no-print" style="margin-top:2rem;">
    <button onclick="window.print()" style="padding:10px 24px; background:#1761a0;
      color:#fff; border:none; border-radius:6px; cursor:pointer; font-size:1rem;">
      Imprimir / Salvar como PDF
    </button>
  </p>
</body>
</html>"""

NOTA_CORRELACAO = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Nota Técnica — Análise de Correlação OC × Saúde</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px;
           margin: 40px auto; padding: 0 2rem; color: #222; line-height: 1.7; }
    h1 { color: #1761a0; border-bottom: 3px solid #6ec1a6; padding-bottom: 8px; }
    h2 { color: #1761a0; margin-top: 2rem; font-size: 1.2rem; }
    code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-size: 0.95em; }
    .formula { background: #f8f9fa; border-left: 4px solid #6ec1a6;
               padding: 12px 16px; margin: 12px 0; border-radius: 4px; font-family: monospace; }
    table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
    th, td { border: 1px solid #dee2e6; padding: 8px 12px; text-align: left; }
    th { background: #e8f4fb; color: #1761a0; }
    @media print {
      a[href]::after { content: none !important; }
      .no-print { display: none; }
    }
  </style>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LHX5DN0BCW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-LHX5DN0BCW', {page_title: document.title + ' | GeoCalor'});
  </script>
</head>
<body>
  <div style="display:flex;align-items:center;gap:24px;margin:16px 0 24px;flex-wrap:wrap;">
    <img src="/assets/sistemas_alerta/images/lagasLogo.png" alt="LAGAS"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/sistemas_alerta/images/geocalorLogo.png" alt="GeoCalor"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/unb.png" alt="UnB"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/fiocruz.png" alt="Fiocruz"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/ufrj_logo.png" alt="UFRJ"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/lmi_logo.png" alt="LMI-Sentinela"
         style="max-height:70px;max-width:140px;object-fit:contain;">
  </div>

  <h1>Nota Técnica — Análise de Correlação: Ondas de Calor × Internações e Óbitos</h1>
  <p><em>Projeto GeoCalor | LAGAS / UnB, Fiocruz/OCS, LASA-UFRJ &amp; LMI-Sentinela</em></p>

  <h2>1. Objetivo</h2>
  <p>Estimar o Risco Relativo (RR) de internações hospitalares (SIH/SUS) e óbitos (SIM)
  associados às ondas de calor (OC) para cada Região Metropolitana brasileira, considerando
  defasagens temporais de 0 a 7 dias após o início do evento.</p>

  <h2>2. Fontes de Dados</h2>
  <ul>
    <li><strong>Dados climáticos:</strong> banco consolidado do Projeto GeoCalor, com séries
    diárias de temperatura máxima, média e mínima, umidade relativa, amplitude térmica e
    Excess Heat Factor (EHF) para 15 Regiões Metropolitanas (2010–2022).</li>
    <li><strong>Dados de saúde:</strong> Sistema de Informações Hospitalares (SIH/SUS) e
    Sistema de Informações sobre Mortalidade (SIM/DATASUS), agrupados por data de internação
    ou ocorrência e Região Metropolitana.</li>
  </ul>

  <h2>3. Definição de Onda de Calor</h2>
  <p>Utilizou-se o critério do <strong>Excess Heat Factor (EHF)</strong>
  (Nairn &amp; Fawcett, 2015): período de 3 ou mais dias consecutivos com EHF &gt; 0.
  A variável binária <code>isHW</code> (1 = dia de OC, 0 = dia sem OC) foi a exposição
  principal do modelo.</p>

  <h2>4. Modelo Estatístico</h2>
  <p>O RR foi estimado por um modelo de
  <strong>Regressão Binomial Negativa com Modelo de Defasagem Distribuída Não-Linear
  (DLNM — Distributed Lag Non-Linear Model)</strong>:</p>

  <div class="formula">
    N_TOTAL ~ cb_hw_lag7 + ns(DT_INTER, df=df_time) + ns(UmidadeMed, df=3)
            + ns(thermalRange, df=3) + dow_f
  </div>

  <p>Onde:</p>
  <ul>
    <li><code>cb_hw_lag7</code>: crossbasis da variável <code>isHW</code>, com função
    linear na dimensão da exposição e spline natural (3 df) na dimensão do lag (lag máximo = 7 dias);</li>
    <li><code>ns(DT_INTER, df=df_time)</code>: spline natural para tendência temporal e
    sazonalidade (7 df por ano × número de anos = até 70 df para séries de 10 anos);</li>
    <li><code>ns(UmidadeMed, df=3)</code>: spline natural para não-linearidade da umidade relativa;</li>
    <li><code>ns(thermalRange, df=3)</code>: spline natural para amplitude térmica;</li>
    <li><code>dow_f</code>: fator do dia da semana (segunda a domingo).</li>
  </ul>

  <h2>5. Estimativa do RR e Intervalos de Confiança</h2>
  <p>As predições foram obtidas com a função <code>crosspred()</code> do pacote
  <code>dlnm</code>, com referência em <code>isHW = 0</code> (dias sem onda de calor).
  Os RR por defasagem correspondem à razão entre as contagens previstas em dias de OC
  e em dias sem OC, ajustada por todos os confundidores do modelo.</p>
  <p>Os Intervalos de Confiança de 95% (IC 95%) derivam dos erros-padrão do modelo
  Binomial Negativo em escala log, transformados de volta à escala original via
  exponenciação.</p>

  <h2>6. Período e Exclusões</h2>
  <table>
    <tr><th>RM</th><th>Período analisado</th><th>Observação</th></tr>
    <tr><td>Recife</td><td>2010–2022</td><td>Período completo disponível</td></tr>
    <tr><td>Demais RMs (14)</td><td>2010–2019</td><td>Anos COVID (2020–2022) excluídos</td></tr>
  </table>
  <p>A exclusão do período COVID para a maioria das RMs visa evitar distorções causadas
  pela pandemia no volume de internações e óbitos.</p>

  </ul>

  <p class="no-print" style="margin-top:2rem;">
    <button onclick="window.print()" style="padding:10px 24px; background:#1761a0;
      color:#fff; border:none; border-radius:6px; cursor:pointer; font-size:1rem;">
      &#x1F5A8; Imprimir / Salvar como PDF
    </button>
  </p>
</body>
</html>"""

NOTA_TEMPERATURAS = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Nota Técnica — Temperaturas e Anomalias</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px;
           margin: 40px auto; padding: 0 2rem; color: #222; line-height: 1.7; }
    h1 { color: #1761a0; border-bottom: 3px solid #6ec1a6; padding-bottom: 8px; }
    h2 { color: #1761a0; margin-top: 2rem; font-size: 1.2rem; }
    code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-size: 0.95em; }
    .formula { background: #f8f9fa; border-left: 4px solid #6ec1a6;
               padding: 12px 16px; margin: 12px 0; border-radius: 4px; font-family: monospace; }
    @media print {
      a[href]::after { content: none !important; }
      .no-print { display: none; }
    }
  </style>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LHX5DN0BCW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-LHX5DN0BCW', {page_title: document.title + ' | GeoCalor'});
  </script>
</head>
<body>
  <div style="display:flex;align-items:center;gap:24px;margin:16px 0 24px;flex-wrap:wrap;">
    <img src="/assets/sistemas_alerta/images/lagasLogo.png" alt="LAGAS"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/sistemas_alerta/images/geocalorLogo.png" alt="GeoCalor"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/unb.png" alt="UnB"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/fiocruz.png" alt="Fiocruz"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/ufrj_logo.png" alt="UFRJ"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/lmi_logo.png" alt="LMI-Sentinela"
         style="max-height:70px;max-width:140px;object-fit:contain;">
  </div>
  <h1>Nota Técnica — Análise de Temperaturas Diárias</h1>
  <p><em>Projeto GeoCalor | LAGAS / UnB, Fiocruz/OCS, LASA-UFRJ &amp; LMI-Sentinela</em></p>

  <h2>1. Fontes de Dados</h2>
  <p>Os dados meteorológicos são provenientes de estações do <strong>INMET</strong>
  (Instituto Nacional de Meteorologia) e do <strong>ICEA</strong>, abrangendo
  15 Regiões Metropolitanas do Brasil no período de <strong>1981 a 2025</strong>.</p>
  <p>Variáveis utilizadas: temperatura máxima (<code>tempMax</code>), temperatura média
  (<code>tempMed</code>), temperatura mínima (<code>tempMin</code>) e umidade relativa
  (<code>HumidadeMed</code>), todas em base diária.</p>

  <h2>2. Tratamento de Lacunas de Dados</h2>
  <p>As lacunas de dados foram preenchidas calculando a temperatura média diária a partir
  da média entre o valor máximo e o valor mínimo do dia (<code>(tempMax + tempMin) / 2</code>),
  ao invés de utilizar a temperatura média compensada fornecida diretamente pelo INMET ou ICEA.</p>

  <h2>3. Amplitude Térmica Diária</h2>
  <p>Calculada como a diferença entre a temperatura máxima e mínima do dia:</p>
  <div class="formula">Amplitude = tempMax − tempMin</div>
  <p>A linha tracejada nos gráficos representa a <strong>média móvel de 30 dias</strong>,
  utilizada para suavizar a variabilidade diária e evidenciar tendências sazonais.</p>

  <h2>4. Anomalia de Temperatura Mensal</h2>
  <p>A anomalia é calculada a partir da média diária: o valor do dia específico menos a
  média daquele dia para todos os anos. Por exemplo, a anomalia do dia 01/01/2000 é a
  temperatura máxima desse dia, menos a média das temperaturas máximas de todos os dias
  01/01 de todos os anos.</p>
  <div class="formula">
    Anomalia<sub>d</sub> = T<sub>d</sub> − T̄<sub>dia-histórico</sub>
  </div>
  <p>Barras <span style="color:#c0392b"><strong>vermelhas</strong></span> indicam meses
  com temperatura acima da média histórica; barras
  <span style="color:#2b7eb3"><strong>azuis</strong></span> indicam meses abaixo.</p>

  <h2>5. Limitações</h2>
  <ul>
    <li>Dados de estações pontuais (não gridados), podendo não representar
    toda a variabilidade espacial da RM.</li>
    <li>Lacunas temporais em algumas séries foram preenchidas calculando a média diária
    a partir do valor máximo e mínimo, ao invés da média compensada fornecida pelo INMET e ICEA.</li>
    <li>O período pós-2020 pode conter dados parcialmente revisados pelo INMET.</li>
  </ul>

  <p style="margin-top:3rem; font-size:0.85rem; color:#888;">
    Gerado pelo Dashboard GeoCalor — LAGAS/UnB, Fiocruz/OCS, LASA-UFRJ &amp; LMI-Sentinela<br>
    Para citar: utilize as referências bibliográficas disponíveis no dashboard.
  </p>

  <p class="no-print" style="margin-top:2rem;">
    <button onclick="window.print()" style="padding:10px 24px; background:#1761a0;
      color:#fff; border:none; border-radius:6px; cursor:pointer; font-size:1rem;">
      Imprimir / Salvar como PDF
    </button>
  </p>
</body>
</html>"""

NOTA_ONDAS = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Nota Técnica — Ondas de Calor e EHF</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px;
           margin: 40px auto; padding: 0 2rem; color: #222; line-height: 1.7; }
    h1 { color: #1761a0; border-bottom: 3px solid #6ec1a6; padding-bottom: 8px; }
    h2 { color: #1761a0; margin-top: 2rem; font-size: 1.2rem; }
    code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; }
    .formula { background: #f8f9fa; border-left: 4px solid #6ec1a6;
               padding: 12px 16px; margin: 12px 0; border-radius: 4px;
               font-family: monospace; font-size: 0.97em; }
    table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
    th, td { border: 1px solid #dee2e6; padding: 8px 12px; text-align: left; }
    th { background: #eaf6fb; color: #1761a0; }
    @media print { a[href]::after { content: none !important; }
                   .no-print { display: none; } }
  </style>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LHX5DN0BCW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-LHX5DN0BCW', {page_title: document.title + ' | GeoCalor'});
  </script>
</head>
<body>
  <div style="display:flex;align-items:center;gap:24px;margin:16px 0 24px;flex-wrap:wrap;">
    <img src="/assets/sistemas_alerta/images/lagasLogo.png" alt="LAGAS"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/sistemas_alerta/images/geocalorLogo.png" alt="GeoCalor"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/unb.png" alt="UnB"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/fiocruz.png" alt="Fiocruz"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/ufrj_logo.png" alt="UFRJ"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/lmi_logo.png" alt="LMI-Sentinela"
         style="max-height:70px;max-width:140px;object-fit:contain;">
  </div>
  <h1>Nota Técnica — Ondas de Calor e Índice EHF</h1>
  <p><em>Projeto GeoCalor | LAGAS / UnB, Fiocruz/OCS, LASA-UFRJ &amp; LMI-Sentinela</em></p>

  <h2>1. Definição de Onda de Calor</h2>
  <p>Neste projeto, uma <strong>Onda de Calor (OC)</strong> é definida como um período
  de <strong>3 ou mais dias consecutivos</strong> nos quais o Fator de Excesso de
  Calor (EHF) apresenta valores positivos, indicando condições de calor excessivo
  para a população local.</p>

  <h2>2. Fator de Excesso de Calor (EHF)</h2>
  <p>O <strong>Excess Heat Factor (EHF)</strong> foi proposto por Nairn e Fawcett (2015)
  e é amplamente utilizado em estudos de saúde e clima no Brasil e no mundo.</p>
  <p>O índice combina dois sub-índices:</p>

  <div class="formula">
    <strong>EHI<sub>sig</sub></strong> — Significância em relação ao percentil 95 histórico:<br>
    EHI<sub>sig</sub> = ((T<sub>i</sub> + T<sub>i+1</sub> + T<sub>i+2</sub>) / 3) − T<sub>95</sub><br><br>
    <strong>EHI<sub>accl</sub></strong> — Capacidade de aclimatação (últimos 30 dias):<br>
    EHI<sub>accl</sub> = ((T<sub>i</sub> + T<sub>i+1</sub> + T<sub>i+2</sub>) / 3) − ((T<sub>i−1</sub> + ... + T<sub>i−30</sub>) / 30)<br><br>
    <strong>EHF</strong> = EHI<sub>sig</sub> × max(1, EHI<sub>accl</sub>)
  </div>

  <p>onde T<sub>95</sub> é o percentil 95 das temperaturas médias diárias calculado
  sobre um período de referência de 30 anos, e T<sub>i</sub> é a temperatura média
  do dia <em>i</em>.</p>

  <h2>3. Classificação por Intensidade</h2>
  <p>As classes de intensidade são definidas a partir de múltiplos do percentil 85
  de todos os valores positivos do EHF (denominado <strong>EHF85</strong>):</p>
  <table>
    <thead><tr><th>Classificação</th><th>Critério (EHF)</th></tr></thead>
    <tbody>
      <tr><td>Baixa Intensidade</td><td>0 &lt; EHF ≤ EHF85</td></tr>
      <tr><td>Severa</td><td>EHF85 &lt; EHF ≤ 3 × EHF85</td></tr>
      <tr><td>Extrema</td><td>EHF &gt; 3 × EHF85</td></tr>
    </tbody>
  </table>

  <h2>4. Gráficos Disponíveis</h2>
  <ul>
    <li><strong>Gráfico polar:</strong> distribuição mensal da frequência de dias de OC.</li>
    <li><strong>Calendário de OC:</strong> visualização interativa dia a dia, com intensidade.</li>
    <li><strong>Temperatura e OC:</strong> série temporal com destaques para dias de OC e picos acima do T95.</li>
    <li><strong>EHF diário:</strong> série do índice com limiar de OC em zero.</li>
    <li><strong>Umidade e OC:</strong> série de umidade relativa com realce dos dias de OC.</li>
    <li><strong>Mapa de calor (heatmap):</strong> frequência de dias/eventos por cidade e ano.</li>
  </ul>

  <h2>5. Fontes e Referências</h2>
  <ul>
    <li>Nairn, J., &amp; Fawcett, R. (2015). The Excess Heat Factor: A Metric for Heatwave
    Intensity and its Use in Classifying Heatwave Severity. <em>Int. J. Environ. Res.
    Public Health</em>, 12(1), 227–253.</li>
    <li>Dados meteorológicos: INMET e ICEA (1981–2025).</li>
    <li>Regiões Metropolitanas: IBGE.</li>
  </ul>

  <p class="no-print" style="margin-top:2.5rem;">
    <button onclick="window.print()" style="padding:10px 24px; background:#1761a0;
      color:#fff; border:none; border-radius:6px; cursor:pointer; font-size:1rem;">
      Imprimir / Salvar como PDF
    </button>
  </p>
</body>
</html>"""

NOTA_SIH_SIM = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Nota Técnica — SIH/SIM</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 860px;
           margin: 40px auto; padding: 0 2rem; color: #222; line-height: 1.7; }
    h1 { color: #1761a0; border-bottom: 3px solid #6ec1a6; padding-bottom: 8px; }
    h2 { color: #1761a0; margin-top: 2rem; font-size: 1.2rem; }
    h3 { color: #2b9eb3; margin-top: 1.4rem; font-size: 1rem; }
    code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-size: 0.95em; }
    .formula { background: #f8f9fa; border-left: 4px solid #6ec1a6;
               padding: 12px 16px; margin: 12px 0; border-radius: 4px; font-family: monospace; }
    .chart-box { background: #eaf6fb; border: 1px solid #b3d6e6; border-radius: 8px;
                 padding: 12px 16px; margin: 14px 0; }
    .chart-box strong { color: #1761a0; }
    table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
    th, td { border: 1px solid #dee2e6; padding: 8px 12px; text-align: left; }
    th { background: #eaf6fb; color: #1761a0; }
    @media print { a[href]::after { content: none !important; }
                   .no-print { display: none; } }
  </style>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LHX5DN0BCW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-LHX5DN0BCW', {page_title: document.title + ' | GeoCalor'});
  </script>
</head>
<body>
  <div style="display:flex;align-items:center;gap:24px;margin:16px 0 24px;flex-wrap:wrap;">
    <img src="/assets/sistemas_alerta/images/lagasLogo.png" alt="LAGAS"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/sistemas_alerta/images/geocalorLogo.png" alt="GeoCalor"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/unb.png" alt="UnB"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/fiocruz.png" alt="Fiocruz"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/ufrj_logo.png" alt="UFRJ"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/lmi_logo.png" alt="LMI-Sentinela"
         style="max-height:70px;max-width:140px;object-fit:contain;">
  </div>

  <h1>Nota Técnica — Sistema de Informações SIH/SIM</h1>
  <p><em>Projeto GeoCalor | LAGAS / UnB, Fiocruz/OCS, LASA-UFRJ &amp; LMI-Sentinela</em></p>

  <h2>1. Fontes de Dados</h2>
  <p>Esta página utiliza os microdados dos seguintes sistemas do DATASUS/Ministério da Saúde:</p>
  <ul>
    <li><strong>SIH — Sistema de Informações Hospitalares:</strong> registros de internações
    hospitalares do SUS. Cobre o período de <strong>2010 a 2025</strong> para as Regiões
    Metropolitanas selecionadas. Cada registro corresponde a uma Autorização de Internação
    Hospitalar (AIH).</li>
    <li><strong>SIM — Sistema de Informações sobre Mortalidade:</strong> registros de óbitos
    ocorridos no território nacional. Cobre o período de <strong>2010 a 2025</strong>.
    Cada registro corresponde a uma Declaração de Óbito (DO).</li>
  </ul>

  <h2>2. Grupos de Causas (CID-10)</h2>
  <table>
    <thead><tr><th>Grupo</th><th>CID-10 (capítulo)</th><th>Descrição</th></tr></thead>
    <tbody>
      <tr><td>Doenças cardiovasculares</td><td>Cap. IX (I00–I99)</td>
          <td>Doenças do aparelho circulatório: cardiopatias, AVC, hipertensão, etc.</td></tr>
      <tr><td>Doenças respiratórias</td><td>Cap. X (J00–J99)</td>
          <td>Doenças do aparelho respiratório: pneumonia, DPOC, asma, etc.</td></tr>
    </tbody>
  </table>

  <h2>3. Abrangência Geográfica</h2>
  <p>Os dados cobrem <strong>15 Regiões Metropolitanas (RMs)</strong> brasileiras,
  selecionadas por sua relevância populacional e disponibilidade de dados completos.
  A análise considera o município de movimentação (SIH) ou de residência (SIM).</p>

  <h2>4. Cálculo das Taxas</h2>
  <p>As taxas anuais são calculadas por <strong>1.000 habitantes</strong> usando
  estimativas populacionais intermediárias do IBGE:</p>
  <div class="formula">
    Taxa<sub>ano</sub> = (N° de internações ou óbitos / População da RM) × 1.000
  </div>
  <p>Quando a estimativa exata do ano não está disponível, utiliza-se a do ano mais
  próximo disponível na base de população.</p>

  <h2>5. Descrição dos Gráficos</h2>

  <div class="chart-box">
    <strong>Caráter de internação (SIH)</strong>
    <p>Distribuição das internações conforme o tipo de admissão: <em>Eletivo</em>
    (internação programada e não urgente) ou <em>Urgência/Emergência</em> (admissão
    não planejada por condição aguda). Evidencia o perfil de demanda do sistema de saúde.</p>
  </div>

  <div class="chart-box">
    <strong>Especialidade do leito (SIH)</strong>
    <p>As 12 especialidades de leito mais utilizadas nas internações selecionadas.
    Inclui leitos clínicos, cirúrgicos, pediátricos, UTI adulto, UTI coronariana e
    outros. Permite identificar a complexidade assistencial das internações.</p>
  </div>

  <div class="chart-box">
    <strong>Local do óbito (SIM)</strong>
    <p>Distribuição dos óbitos conforme o local de ocorrência: Hospital, Domicílio,
    Via pública, Outro estabelecimento de saúde ou Outros. Indica o contexto
    assistencial e social em que os óbitos ocorrem.</p>
  </div>

  <div class="chart-box">
    <strong>Estado civil (SIM)</strong>
    <p>Distribuição dos óbitos por estado civil autodeclarado na Declaração de Óbito:
    Solteiro, Casado, Viúvo, Separado judicialmente ou União consensual. Permite
    análise de determinantes sociais associados à mortalidade.</p>
  </div>

  <div class="chart-box">
    <strong>Raça/cor</strong>
    <p>Distribuição proporcional das internações ou óbitos por raça/cor autodeclarada,
    conforme a classificação do IBGE: Branca, Parda, Preta, Amarela e Indígena.
    Ferramenta fundamental para análise de equidade em saúde.</p>
  </div>

  <div class="chart-box">
    <strong>Série temporal mensal por ano</strong>
    <p>Gráfico facetado com um painel por ano (até 7 colunas), replicando o
    <em>grafico4</em> do script de infográfico da RIDE-DF. Cada painel exibe uma
    <strong>linha preta</strong> com o volume mensal de internações ou óbitos (eixo Y
    livre entre painéis, equivalente a <code>scales="free_y"</code> do R). Sobre cada
    painel são sobrepostas <strong>cinco linhas tracejadas coloridas</strong>
    correspondendo aos limiares de risco calculados por
    <strong>quebras naturais de Fisher/Jenks</strong>
    (<code>classIntervals(style="fisher", n=5)</code> no R;
    <code>jenkspy.jenks_breaks(n_classes=5)</code> no Python) sobre todos os volumes
    mensais do período. Os cinco limiares armazenados correspondem aos primeiros cinco
    dos seis valores retornados pelo algoritmo (equivalente a <code>epi[1:5]</code>
    em R indexação 1-based), representando as categorias:</p>
    <table>
      <thead><tr><th>Categoria</th><th>Cor</th><th>Significado</th></tr></thead>
      <tbody>
        <tr><td>Sem risco</td><td style="background:#000099;color:#fff;padding:2px 8px;">#000099</td><td>Volume abaixo do limiar mínimo histórico</td></tr>
        <tr><td>Segurança</td><td style="background:#009900;color:#fff;padding:2px 8px;">#009900</td><td>Volume dentro do intervalo esperado</td></tr>
        <tr><td>Baixo</td><td style="background:#FFD166;padding:2px 8px;">#FFD166</td><td>Elevação moderada em relação à distribuição histórica</td></tr>
        <tr><td>Moderado</td><td style="background:#ff8000;color:#fff;padding:2px 8px;">#ff8000</td><td>Volume acima da maioria dos meses históricos</td></tr>
        <tr><td>Alto</td><td style="background:#cc0000;color:#fff;padding:2px 8px;">#cc0000</td><td>Volume entre os mais altos registrados</td></tr>
      </tbody>
    </table>
    <p>Quando há menos de 5 valores únicos disponíveis, os limiares são calculados por
    quantis uniformes como fallback.</p>
  </div>

  <div class="chart-box">
    <strong>Taxa mensal por ano (por 10.000 hab.)</strong>
    <p>Gráfico de barras facetado por ano (3 colunas por linha, equivalente a
    <code>facet_wrap(ncol=3)</code> do R), replicando o <em>grafico6</em> do script de
    infográfico. Cada barra representa a <strong>taxa mensal por 10.000 habitantes</strong>,
    calculada como:</p>
    <div class="formula">
      Taxa<sub>mês,ano</sub> = (N° de internações ou óbitos no mês / População da RM) × 10.000
    </div>
    <p>A população utilizada é a estimativa do IBGE para o ano correspondente
    (ou o ano mais próximo disponível em <code>populacao_RM.parquet</code>).
    O eixo Y é independente entre painéis (<code>shared_yaxes=False</code>), permitindo
    visualizar a sazonalidade relativa de cada ano mesmo quando os volumes absolutos
    diferem. As cores das barras seguem a paleta cromática do dashboard.</p>
  </div>

  <div class="chart-box">
    <strong>Sazonalidade mensal — Mapa de calor (ano × mês)</strong>
    <p>Cada célula representa o <strong>número absoluto</strong> de internações ou óbitos
    naquele mês e ano específico. Cores mais escuras indicam maior volume. Permite
    identificar sazonalidade (ex.: picos respiratórios no inverno) e tendências de
    longo prazo. Os valores são contagens brutas, não taxas populacionais.</p>
  </div>

  <div class="chart-box">
    <strong>Taxa anual por 1.000 hab.</strong>
    <p>Evolução da taxa de internações ou óbitos ao longo dos anos, ajustada pela
    população da RM. Permite comparar a carga de doença entre RMs de tamanhos
    diferentes e identificar tendências temporais independente do crescimento
    populacional.</p>
  </div>

  <div class="chart-box">
    <strong>Internações/óbitos por sexo</strong>
    <p>Contagem absoluta de internações ou óbitos separada por sexo (Masculino e
    Feminino) ao longo dos anos. Evidencia diferenças no padrão de adoecimento e
    mortalidade entre os sexos para cada grupo de causa.</p>
  </div>

  <div class="chart-box">
    <strong>Pirâmide etária por sexo</strong>
    <p>Gráfico de barras horizontais espelhadas (pirâmide populacional), replicando o
    <em>grafico10</em> do script de infográfico. O eixo horizontal representa a
    <strong>proporção em relação ao total geral</strong> de internações ou óbitos
    (masculino à esquerda com valores negativos; feminino à direita). As faixas etárias
    são ordenadas de &lt;1 ano até &gt;80 anos. O eixo exibe percentuais simétricos
    (ex.: 10% – 5% – 0 – 5% – 10%). Esta visualização permite identificar os grupos
    etários e de sexo mais afetados e comparar o perfil etário entre internações
    (SIH) e óbitos (SIM) para cada causa.</p>
  </div>

  <div class="chart-box">
    <strong>Distribuição por faixa etária</strong>
    <p>Distribuição proporcional das internações ou óbitos por faixa etária. Identifica
    os grupos mais afetados pelas doenças cardiovasculares e respiratórias. Para o SIH,
    considera a idade no momento da internação; para o SIM, a idade ao óbito.</p>
  </div>

  <div class="chart-box">
    <strong>Mapa coroplético — Taxa por município</strong>
    <p>Mapa temático mostrando a taxa de internações ou óbitos por 1.000 habitantes
    em cada município da RM para o ano selecionado. Municípios com taxas mais altas
    aparecem em tons mais escuros de azul. Municípios sem dados no ano selecionado
    aparecem sem coloração.</p>
  </div>

  <p style="margin-top:3rem; font-size:0.85rem; color:#888;">
    Gerado pelo Dashboard GeoCalor — LAGAS/UnB, Fiocruz/OCS, LASA-UFRJ &amp; LMI-Sentinela<br>
    Para citar: utilize as referências bibliográficas disponíveis no dashboard.
  </p>

  <p class="no-print" style="margin-top:2rem;">
    <button onclick="window.print()" style="padding:10px 24px; background:#1761a0;
      color:#fff; border:none; border-radius:6px; cursor:pointer; font-size:1rem;">
      Imprimir / Salvar como PDF
    </button>
  </p>
</body>
</html>"""

NOTA_ATUALIZACAO_2025 = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Nota Técnica — O que Mudou em 2024-2025</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 860px;
           margin: 40px auto; padding: 0 2rem; color: #222; line-height: 1.7; }
    h1 { color: #1761a0; border-bottom: 3px solid #6ec1a6; padding-bottom: 8px; }
    h2 { color: #1761a0; margin-top: 2rem; font-size: 1.2rem; }
    h3 { color: #2b9eb3; margin-top: 1.3rem; font-size: 0.98rem; }
    .callout { background: #eaf6fb; border-radius: 8px; padding: 12px 16px; margin: 12px 0; }
    .callout.warn { background: #fdf4e9; }
    .callout strong { color: #1761a0; }
    .callout.warn strong { color: #a3630f; }
    table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.92rem; }
    th, td { border: 1px solid #dee2e6; padding: 7px 11px; text-align: right; }
    th:first-child, td:first-child { text-align: left; }
    th { background: #e8f4fb; color: #1761a0; font-size: 0.82rem; text-transform: uppercase; }
    tr.hi td { background: #f4f9fb; font-weight: 600; }
    .stat-row { display: flex; flex-wrap: wrap; gap: 0.75rem; margin: 1.2rem 0 1.6rem; }
    .stat { flex: 1 1 190px; background: #fff; border: 1px solid #dee2e6; border-radius: 8px;
            padding: 0.85rem 1rem; }
    .stat .n { font-size: 1.35rem; font-weight: 700; color: #1761a0; display: block; }
    .stat .l { font-size: 0.78rem; color: #5a6a7a; margin-top: 0.2rem; display: block; }
    caption { text-align: left; font-size: 0.82rem; color: #5a6a7a; margin-bottom: 0.4rem;
              caption-side: top; }
    .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.1rem 0 0.4rem; }
    .chart-box2 { background: #fff; border: 1px solid #dee2e6; border-radius: 8px;
                  padding: 0.9rem 1rem 0.7rem; }
    .chart-box2 .ct { font-size: 0.86rem; font-weight: 700; color: #222; }
    .chart-box2 .cs { font-size: 0.74rem; color: #5a6a7a; margin-bottom: 0.35rem; }
    .chart-box2 svg { width: 100%; height: auto; display: block; }
    @media (max-width: 620px) { .chart-grid { grid-template-columns: 1fr; } }
    .ctrl-bar { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;
                background: #f4f9fb; border-radius: 8px; padding: 0.7rem 0.9rem; margin: 1.2rem 0 0; }
    .ctrl-bar label { font-size: 0.86rem; font-weight: 600; color: #1761a0; }
    .ctrl-bar select { font-family: 'Segoe UI', Arial, sans-serif; font-size: 0.92rem; color: #222;
                        background: #fff; border: 1.5px solid #b3d6e6; border-radius: 6px;
                        padding: 0.35rem 0.6rem; cursor: pointer; }
    .ctrl-bar select:focus { outline: 2px solid #2b9eb3; outline-offset: 1px; }
    .rm-note { font-size: 0.82rem; color: #a3630f; background: #fdf4e9; border-radius: 6px;
               padding: 0.5rem 0.8rem; margin: 0.55rem 0 0; }
    .rm-note:empty { display: none; }
    tr.rm-hi td { background: #fdeef0 !important; font-weight: 700; }
    @media print {
      a[href]::after { content: none !important; }
      .no-print { display: none; }
    }
  </style>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LHX5DN0BCW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-LHX5DN0BCW', {page_title: document.title + ' | GeoCalor'});
  </script>
</head>
<body>
  <div style="display:flex;align-items:center;gap:24px;margin:16px 0 24px;flex-wrap:wrap;">
    <img src="/assets/sistemas_alerta/images/lagasLogo.png" alt="LAGAS"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/sistemas_alerta/images/geocalorLogo.png" alt="GeoCalor"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/unb.png" alt="UnB"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/fiocruz.png" alt="Fiocruz"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/ufrj_logo.png" alt="UFRJ"
         style="max-height:70px;max-width:140px;object-fit:contain;">
    <img src="/assets/lmi_logo.png" alt="LMI-Sentinela"
         style="max-height:70px;max-width:140px;object-fit:contain;">
  </div>

  <h1>Nota Técnica — O que Mudou em 2024 e 2025</h1>
  <p><em>Projeto GeoCalor | LAGAS / UnB, Fiocruz/OCS, LASA-UFRJ &amp; LMI-Sentinela</em></p>
  <p>Comparação entre 2024-2025 e o período de referência 2010-2023 nas Regiões Metropolitanas
  monitoradas pelo GeoCalor, a partir dos dados climáticos (EHF) e das razões de mortalidade
  observada/esperada (O/E) por onda de calor.</p>

  <div class="ctrl-bar">
    <label for="rm-select">Ver dados de</label>
    <select id="rm-select"></select>
  </div>
  <p id="rm-note" class="rm-note"></p>

  <div class="stat-row">
    <div class="stat"><span class="n" id="s1n">100</span><span class="l" id="s1l">ondas de calor em
      2024, recorde da série 1981-2025 (+62% vs. média 2010-2023)</span></div>
    <div class="stat"><span class="n" id="s2n">1,46</span><span class="l" id="s2l">razão O/E média
      em 2025, maior valor anual da série</span></div>
    <div class="stat"><span class="n" id="s3n">71,6%</span><span class="l" id="s3l">das ondas de
      2025 com excesso de mortalidade significativo (vs. 42,6% em 2010-2023)</span></div>
    <div class="stat"><span class="n" id="s4n">≈13.700</span><span class="l" id="s4l">óbitos
      atribuíveis a ondas de calor em 2024+2025 (2025 parcial)</span></div>
  </div>

  <h2>1. Metodologia da comparação</h2>
  <p>O período de 2010 a 2023 (14 anos) é usado como linha de base para todas as comparações
  abaixo. Eventos de onda de calor (OC) seguem a definição padrão do projeto: 3 ou mais dias
  consecutivos com EHF positivo, classificados por intensidade a partir do percentil 85 histórico
  (EHF85). A mortalidade atribuível usa a razão Observado/Esperado (O/E) por evento, com IC 95%
  calculado contra a variabilidade histórica do mesmo período do ano (ver Nota Técnica de
  Mortalidade x OC).</p>
  <div class="callout warn">
    <strong>Recife</strong> foi excluída de toda a análise: a estação climática não tem dados
    válidos desde setembro de 2020. <strong>Salvador</strong> segue no agregado nacional, mas não
    tem temperatura válida desde janeiro de 2022 — na prática, sem ondas nem O/E computáveis para
    2022-2025. Selecione as duas RMs individualmente abaixo para ver o que resta de série
    histórica. Detalhes na seção 5.
  </div>

  <h2>2. Ondas de calor: frequência e intensidade</h2>
  <p>2024 foi o ano com mais eventos de onda de calor desde o início da série em 1981: 100 eventos
  nas 14 RMs analisadas, superando o recorde anterior (91, em 2023) pelo segundo ano consecutivo.
  O aumento foi generalizado: 13 das 14 RMs tiveram mais eventos em 2024 do que sua própria média
  2010-2023. Em 2025 a frequência recuou para perto do padrão histórico (56 eventos), mas a
  duração média dos eventos (6,4 dias) segue acima da mediana longa da série.</p>

  <div class="chart-grid">
    <div class="chart-box2">
      <div class="ct">Eventos de onda de calor por ano</div>
      <div class="cs">14 RMs (exclui Recife) · 2010-2025</div>
      <svg id="chart-events" viewBox="0 0 360 190"></svg>
    </div>
    <div class="chart-box2">
      <div class="ct">Anomalia de temperatura média</div>
      <div class="cs">°C em relação à normal 1991-2020</div>
      <svg id="chart-anom" viewBox="0 0 360 190"></svg>
    </div>
  </div>

  <table>
    <thead><tr><th>Período</th><th>Eventos/ano</th><th>Baixa int.</th><th>Severa</th>
      <th>Extrema</th><th>Duração média</th></tr></thead>
    <tbody>
      <tr><td>2010-2023 (média)</td><td>61,6</td><td>59,6</td><td>1,8</td><td>0,2</td><td>6,5 dias</td></tr>
      <tr class="hi"><td>2024</td><td>100</td><td>94</td><td>6</td><td>0</td><td>7,3 dias</td></tr>
      <tr><td>2025*</td><td>56</td><td>52</td><td>4</td><td>0</td><td>6,4 dias</td></tr>
    </tbody>
  </table>

  <h3>Por região metropolitana</h3>
  <table>
    <caption>Eventos em 2024 e 2025 frente à média histórica de cada RM</caption>
    <thead><tr><th>RM</th><th>Média 2010-2023</th><th>2024</th><th>2025</th></tr></thead>
    <tbody id="tbl-rm-body">
      <tr data-city="Cuiabá"><td>Cuiabá</td><td>5,5</td><td>18</td><td>11</td></tr>
      <tr data-city="Manaus"><td>Manaus</td><td>5,6</td><td>14</td><td>5</td></tr>
      <tr data-city="São Paulo"><td>São Paulo</td><td>4,3</td><td>11</td><td>4</td></tr>
      <tr data-city="Belo Horizonte"><td>Belo Horizonte</td><td>4,8</td><td>11</td><td>6</td></tr>
      <tr data-city="Porto Velho"><td>Porto Velho</td><td>4,5</td><td>9</td><td>4</td></tr>
      <tr data-city="Goiânia"><td>Goiânia</td><td>5,3</td><td>6</td><td>10</td></tr>
      <tr data-city="Curitiba"><td>Curitiba</td><td>3,3</td><td>6</td><td>3</td></tr>
      <tr data-city="Fortaleza"><td>Fortaleza</td><td>2,3</td><td>6</td><td>1</td></tr>
      <tr data-city="Florianópolis"><td>Florianópolis</td><td>3,9</td><td>5</td><td>5</td></tr>
      <tr data-city="Porto Alegre"><td>Porto Alegre</td><td>4,4</td><td>5</td><td>0</td></tr>
      <tr data-city="Brasília"><td>Brasília</td><td>4,2</td><td>4</td><td>6</td></tr>
      <tr data-city="Belém"><td>Belém</td><td>7,9</td><td>3</td><td>0</td></tr>
      <tr data-city="Rio de Janeiro"><td>Rio de Janeiro</td><td>3,1</td><td>2</td><td>1</td></tr>
      <tr data-city="Salvador"><td>Salvador</td><td>2,6</td><td>0</td><td>0</td></tr>
    </tbody>
  </table>

  <h2>3. Temperatura e EHF</h2>
  <p>A anomalia média de temperatura em 2024 (+1,12°C frente à normal climatológica 1991-2020) foi
  mais que o triplo da média 2010-2023 (+0,30°C), e o percentual de dias em onda de calor quase
  dobrou (14,2% contra 7,8%). Em 2025 esses indicadores recuaram para perto da média histórica
  (+0,29°C, 7,2% dos dias), acompanhando a queda na frequência de eventos.</p>
  <table>
    <thead><tr><th>Período</th><th>Temp. máx. média</th><th>Temp. média</th><th>Anomalia</th>
      <th>% dias em OC</th></tr></thead>
    <tbody>
      <tr><td>2010-2023 (média)</td><td>29,1 °C</td><td>24,5 °C</td><td>+0,30 °C</td><td>7,8%</td></tr>
      <tr class="hi"><td>2024</td><td>29,7 °C</td><td>25,1 °C</td><td>+1,12 °C</td><td>14,2%</td></tr>
      <tr><td>2025*</td><td>28,9 °C</td><td>24,5 °C</td><td>+0,29 °C</td><td>7,2%</td></tr>
    </tbody>
  </table>

  <h2>4. Mortalidade atribuível: o sinal que não recuou</h2>
  <p>Este é o achado central da nota: mesmo com a frequência de ondas voltando perto da média
  histórica em 2025, a letalidade por onda continuou subindo. A razão O/E média passou de 1,18
  (2010-2023) para 1,40 em 2024 e 1,46 em 2025, o maior valor anual da série. A proporção de ondas
  com excesso estatisticamente significativo saltou de 42,6% (linha de base) para 64,8% em 2024 e
  71,6% em 2025. No critério mais estrito: em 2010-2023, 106 das 531 ondas significativas (20%)
  tiveram efeito protetor (déficit de mortalidade); em 2024 e 2025, nenhuma onda significativa
  teve efeito protetor, todas as 129 foram de excesso.</p>

  <div class="chart-grid">
    <div class="chart-box2">
      <div class="ct">Razão O/E média por ano</div>
      <div class="cs">mortalidade observada / esperada durante a onda</div>
      <svg id="chart-oer" viewBox="0 0 360 190"></svg>
    </div>
    <div class="chart-box2">
      <div class="ct">% de ondas com excesso significativo</div>
      <div class="cs">IC 95% · sobre o total de ondas do ano</div>
      <svg id="chart-sig" viewBox="0 0 360 190"></svg>
    </div>
  </div>

  <table>
    <caption>Série anual: ondas com O/E calculado, % significativas e óbitos atribuíveis</caption>
    <thead><tr><th>Ano</th><th>Ondas</th><th>% signif.</th><th>O/E médio</th>
      <th>Óbitos atrib.</th></tr></thead>
    <tbody>
      <tr><td>2018</td><td>84</td><td>36,9%</td><td>1,13</td><td>1.580</td></tr>
      <tr><td>2019</td><td>120</td><td>45,8%</td><td>1,20</td><td>3.041</td></tr>
      <tr><td>2020</td><td>90</td><td>35,6%</td><td>1,19</td><td>2.213</td></tr>
      <tr><td>2021</td><td>65</td><td>46,2%</td><td>1,23</td><td>1.483</td></tr>
      <tr><td>2022</td><td>74</td><td>59,5%</td><td>1,42</td><td>3.586</td></tr>
      <tr><td>2023</td><td>98</td><td>68,4%</td><td>1,39</td><td>9.311</td></tr>
      <tr class="hi"><td>2024</td><td>125</td><td>64,8%</td><td>1,40</td><td>8.964</td></tr>
      <tr class="hi"><td>2025*</td><td>67</td><td>71,6%</td><td>1,46</td><td>4.732</td></tr>
    </tbody>
  </table>

  <h3>Óbitos atribuíveis por RM, 2024+2025 combinados</h3>
  <table>
    <thead><tr><th>RM</th><th>Ondas</th><th>O/E médio</th><th>Óbitos atrib.</th></tr></thead>
    <tbody id="tbl-obitos-body">
      <tr data-city="São Paulo"><td>São Paulo</td><td>18</td><td>1,3</td><td>5.641</td></tr>
      <tr data-city="Manaus"><td>Manaus</td><td>22</td><td>1,7</td><td>1.975</td></tr>
      <tr data-city="Goiânia"><td>Goiânia</td><td>26</td><td>1,3</td><td>1.905</td></tr>
      <tr data-city="Belo Horizonte"><td>Belo Horizonte</td><td>21</td><td>1,2</td><td>944</td></tr>
      <tr data-city="Brasília"><td>Brasília</td><td>15</td><td>1,5</td><td>902</td></tr>
      <tr data-city="Curitiba"><td>Curitiba</td><td>10</td><td>2,3</td><td>673</td></tr>
      <tr data-city="Cuiabá"><td>Cuiabá</td><td>28</td><td>1,5</td><td>667</td></tr>
      <tr data-city="Fortaleza"><td>Fortaleza</td><td>6</td><td>1,3</td><td>340</td></tr>
      <tr data-city="Rio de Janeiro"><td>Rio de Janeiro</td><td>3</td><td>1,1</td><td>207</td></tr>
      <tr data-city="Florianópolis"><td>Florianópolis</td><td>10</td><td>1,5</td><td>179</td></tr>
      <tr data-city="Porto Velho"><td>Porto Velho</td><td>15</td><td>1,4</td><td>118</td></tr>
      <tr data-city="Porto Alegre"><td>Porto Alegre</td><td>7</td><td>1,1</td><td>112</td></tr>
      <tr data-city="Belém"><td>Belém</td><td>11</td><td>1,0</td><td>32</td></tr>
    </tbody>
  </table>
  <p style="font-size:0.85rem;color:#5a6a7a;">Recife e Salvador não têm ondas com O/E calculado
  desde, respectivamente, 2020 e 2022. Curitiba tem o maior O/E médio do período apesar do volume
  moderado de eventos.</p>

  <h2>5. Leitura dos resultados e limitações</h2>
  <p>A frequência de ondas de calor e a letalidade por onda se moveram em direções diferentes
  entre 2024 e 2025, um sinal que se perde se o acompanhamento olhar apenas para a contagem de
  eventos. 2024 combinou os dois: recorde de eventos e recorde de anomalia de temperatura. 2025
  recuou na frequência e na temperatura, praticamente de volta à média histórica, mas a razão O/E
  e o percentual de ondas significativas continuaram subindo, dando continuidade a uma tendência
  em curso desde 2022. O período coincide com o El Niño de 2023-2024, um dos mais fortes já
  registrados, seguido por transição para La Niña em 2024-2025; um contexto plausível para o pico
  de 2024, mas esta nota não testa atribuição causal formal a esse fenômeno.</p>
  <div class="callout">
    <strong>Limitações:</strong> Recife sem dado climático válido desde setembro de 2020
    (excluída da série); Salvador sem temperatura válida desde janeiro de 2022, por isso sem
    ondas nem O/E computáveis de 2022 em diante; Belém e Porto Alegre não registraram eventos de
    OC em 2025 pelos critérios de EHF atuais; anos com menos ondas (ex.: 2013, 2021) têm
    intervalos de confiança mais largos por evento, o que deve ser considerado em comparações
    ano a ano.
  </div>

  <h2>6. Fontes</h2>
  <p>Dados climáticos INMET/ICEA (1981-2025), Fator de Excesso de Calor (EHF) conforme Nairn
  &amp; Fawcett (2015), normal climatológica de referência 1991-2020; microdados de mortalidade
  SIM e internações SIH, DATASUS/Ministério da Saúde (2010-2025). Metodologia completa de O/E e
  de eventos de OC nas Notas Técnicas de Mortalidade x OC e de Ondas de Calor/EHF do dashboard.</p>

  <p class="no-print" style="margin-top:2rem;">
    <button onclick="window.print()" style="padding:10px 24px; background:#1761a0;
      color:#fff; border:none; border-radius:6px; cursor:pointer; font-size:1rem;">
      Imprimir / Salvar como PDF
    </button>
  </p>

  <script>
  (function () {
    var NS = "http://www.w3.org/2000/svg";
    var CIDADES = {"__GERAL__":{"label":"Geral (14 RMs)","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[59,57,66,39,42,76,85,64,40,83,69,40,51,91,100,56],"anom":[0.15,-0.19,0.35,-0.14,0.16,0.59,0.38,0.41,0.26,0.78,0.39,0.03,0.06,0.94,1.12,0.29],"oer":[1.016,1.02,1.196,1.055,1.2,1.162,1.162,1.107,1.128,1.199,1.191,1.234,1.423,1.391,1.398,1.462],"sig":[35.1,35.0,38.6,22.0,43.5,44.1,42.3,41.2,36.9,45.8,35.6,46.2,59.5,68.4,64.8,71.6],"obitos":[213.1,-94.2,1591.1,624.3,3302.9,3173.3,3219.1,1034.6,1580.5,3041.0,2212.6,1482.5,3585.8,9310.6,8963.8,4731.5]},"Belo Horizonte":{"label":"Belo Horizonte","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[5,2,5,3,3,7,7,4,4,8,3,3,1,12,11,6],"anom":[0.17,-0.19,0.06,-0.25,0.49,1.05,0.71,0.09,0.18,1.26,0.31,0.41,0.14,1.3,1.55,0.7],"oer":[1.002,0.915,0.994,0.953,1.087,1.01,1.049,0.982,1.022,1.045,1.079,1.141,1.562,1.174,1.214,1.296],"sig":[14.3,0.0,0.0,14.3,20.0,50.0,14.3,0.0,14.3,16.7,33.3,50.0,100.0,41.7,58.3,77.8],"obitos":[-0.3,-31.4,-8.6,-26.3,71.4,93.1,88.1,-9.5,32.1,114.5,78.0,113.4,139.1,551.4,515.9,428.1]},"Belém":{"label":"Belém","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[13,12,0,0,0,7,15,12,2,8,17,4,7,14,3,0],"anom":[0.46,0.39,-0.02,0.47,0.26,0.75,0.77,0.7,0.7,0.92,1.15,0.68,0.74,1.23,1.71,null],"oer":[0.678,0.714,0.744,0.799,0.797,0.842,0.832,0.797,0.871,0.898,1.053,0.931,1.01,1.941,1.024,null],"sig":[93.3,87.5,75.0,30.0,75.0,54.5,59.1,69.2,53.3,26.3,46.2,21.4,30.8,100.0,9.1,null],"obitos":[-1133.9,-798.3,-100.7,-159.0,-110.4,-481.2,-645.1,-722.1,-390.9,-383.1,418.4,-122.0,-82.3,4049.9,32.0,0]},"Brasília":{"label":"Brasília","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[3,3,4,2,3,8,5,3,3,8,4,3,2,8,4,6],"anom":[0.55,-0.12,0.16,0.2,0.19,1.39,2.13,0.66,0.06,1.11,0.27,0.33,0.42,1.29,1.12,0.57],"oer":[1.067,1.31,1.311,1.144,1.294,1.152,1.07,1.296,1.476,1.242,1.212,1.291,1.341,1.357,1.526,1.457],"sig":[0.0,100.0,75.0,16.7,66.7,25.0,21.4,80.0,100.0,42.9,33.3,100.0,80.0,87.5,100.0,85.7],"obitos":[48.4,74.3,141.7,53.3,190.4,355.3,72.0,252.0,146.5,349.5,195.0,174.7,137.0,811.8,595.3,306.5]},"Cuiabá":{"label":"Cuiabá","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[6,6,3,3,6,5,4,8,2,6,11,4,7,6,18,11],"anom":[0.5,0.54,0.54,-0.05,0.05,0.73,-0.18,0.74,0.19,1.09,2.14,1.35,0.75,2.19,2.48,0.81],"oer":[1.1,1.08,1.731,1.242,1.262,1.317,1.277,1.103,1.346,1.317,1.244,1.126,1.249,1.395,1.47,1.542],"sig":[20.0,0.0,100.0,20.0,33.3,60.0,20.0,11.1,25.0,27.3,25.0,16.7,22.2,40.0,55.0,75.0],"obitos":[60.5,14.8,126.0,24.5,57.5,282.7,40.0,32.3,75.6,101.8,204.7,73.6,41.9,445.1,448.8,218.5]},"Curitiba":{"label":"Curitiba","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[3,1,6,2,1,5,4,2,2,7,3,0,5,5,6,3],"anom":[-0.92,-0.79,0.36,-1.04,-0.2,-0.09,-0.79,-0.36,-0.26,0.23,0.19,-0.81,-0.79,0.2,0.86,-0.64],"oer":[1.412,1.546,1.781,1.574,2.688,1.804,1.938,1.689,1.745,1.808,1.758,null,1.891,0.018,2.25,2.318],"sig":[66.7,100.0,100.0,100.0,100.0,80.0,100.0,66.7,100.0,100.0,100.0,null,75.0,100.0,100.0,100.0],"obitos":[81.8,22.2,214.0,87.7,293.9,217.1,156.5,79.5,141.6,282.7,113.0,0,294.5,-206.2,442.5,230.4]},"Florianópolis":{"label":"Florianópolis","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[2,4,8,3,4,4,4,5,2,7,1,0,6,4,5,5],"anom":[-0.3,-0.4,0.52,-0.59,0.4,0.4,-0.75,0.37,-0.03,0.82,0.18,-0.34,-0.26,0.78,0.34,0.03],"oer":[0.942,1.003,1.112,1.089,1.086,1.289,1.097,1.249,1.324,1.218,0.992,null,1.621,1.348,1.554,1.399],"sig":[0.0,0.0,12.5,0.0,25.0,60.0,20.0,20.0,33.3,28.6,0.0,null,42.9,50.0,80.0,80.0],"obitos":[1.7,-3.5,18.4,1.9,32.1,47.9,10.5,42.5,28.3,46.3,-0.5,0,142.4,64.4,89.0,90.0]},"Fortaleza":{"label":"Fortaleza","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[1,0,0,2,0,0,2,1,2,3,4,11,0,6,6,1],"anom":[-0.16,-1.27,-0.61,-0.21,-0.49,-0.56,0.18,0.07,0.1,0.07,0.29,0.44,-0.01,0.34,0.48,0.07],"oer":[0.748,null,null,1.062,null,null,1.054,null,1.307,1.284,1.135,1.394,null,1.399,1.347,1.362],"sig":[100.0,null,null,0.0,null,null,0.0,null,100.0,100.0,50.0,75.0,null,100.0,100.0,100.0],"obitos":[-17.5,0,0,-2.0,0,0,6.6,0,61.3,57.2,31.4,400.8,0,218.1,317.9,21.8]},"Goiânia":{"label":"Goiânia","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[5,2,4,5,6,8,8,6,6,7,5,2,2,8,6,10],"anom":[0.98,-0.02,0.21,0.05,0.46,1.24,1.07,0.72,0.62,1.32,0.51,0.47,0.52,1.36,1.42,1.43],"oer":[1.187,1.049,1.182,1.071,1.278,1.026,1.135,1.238,1.061,1.235,1.186,1.508,1.544,1.289,1.217,1.288],"sig":[30.0,0.0,28.6,11.1,57.1,33.3,25.0,50.0,0.0,66.7,40.0,100.0,100.0,44.4,61.5,46.2],"obitos":[217.0,14.8,143.9,48.4,316.6,321.7,191.8,275.7,49.4,440.5,285.7,327.6,205.4,637.2,1269.3,635.5]},"Manaus":{"label":"Manaus","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[5,7,7,3,4,10,7,4,6,5,5,2,6,7,14,5],"anom":[0.67,0.14,0.18,0.25,0.27,1.28,0.62,0.36,0.66,0.34,0.61,-0.22,0.42,1.16,1.45,0.4],"oer":[1.08,1.216,1.214,1.016,1.193,1.317,1.475,1.196,1.273,1.571,1.303,1.848,1.796,1.769,1.76,1.724],"sig":[20.0,33.3,42.9,12.5,20.0,57.1,64.3,50.0,44.4,83.3,40.0,87.5,100.0,90.0,100.0,77.8],"obitos":[56.7,96.2,89.3,27.5,162.7,449.7,282.1,190.9,196.9,248.9,230.4,251.5,473.9,1025.3,1366.9,608.5]},"Porto Alegre":{"label":"Porto Alegre","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[2,5,8,2,4,3,7,5,1,6,5,3,5,5,5,0],"anom":[-0.33,-0.2,1.75,-0.26,0.63,0.16,-0.41,1.07,0.12,0.96,0.53,0.13,-0.13,0.83,0.54,-1.18],"oer":[1.396,1.111,1.164,1.178,1.174,1.048,1.071,1.095,1.059,0.994,0.943,1.004,1.125,1.039,1.099,null],"sig":[50.0,16.7,44.4,33.3,25.0,0.0,10.0,25.0,0.0,14.3,0.0,0.0,16.7,20.0,28.6,null],"obitos":[297.1,90.9,273.6,124.3,449.6,10.2,121.1,38.2,48.6,23.5,-41.2,19.5,248.1,28.5,112.0,0]},"Porto Velho":{"label":"Porto Velho","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[3,12,11,0,0,6,7,3,0,1,2,4,4,10,9,4],"anom":[0.37,0.99,1.04,-0.6,-0.75,0.11,0.28,-0.03,-0.3,-0.1,-0.03,-0.4,-0.16,0.69,0.86,0.03],"oer":[0.856,1.053,1.229,1.406,1.802,1.366,1.319,1.254,1.284,1.475,1.391,1.123,1.684,1.329,1.303,1.478],"sig":[16.7,15.4,18.8,0.0,0.0,14.3,11.1,33.3,0.0,0.0,20.0,0.0,50.0,33.3,20.0,20.0],"obitos":[-10.3,46.1,87.2,3.5,11.1,28.6,24.2,16.8,6.5,13.6,22.4,9.1,26.3,63.8,90.3,27.8]},"Rio de Janeiro":{"label":"Rio de Janeiro","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[4,0,3,3,4,6,6,5,3,7,1,1,0,0,2,1],"anom":[-0.29,-1.11,-0.1,0.37,0.64,1.14,0.95,1.32,1.1,1.23,-0.9,-1.14,-0.99,-0.36,-0.06,-0.91],"oer":[1.222,null,1.247,1.158,1.204,1.099,1.177,1.016,1.111,1.069,1.17,1.175,null,1.425,1.101,1.218],"sig":[75.0,null,100.0,100.0,71.4,50.0,83.3,0.0,25.0,57.1,100.0,100.0,null,100.0,50.0,100.0],"obitos":[546.4,0,291.8,197.3,605.2,721.8,986.9,74.6,211.6,388.2,67.6,110.5,0,130.6,98.2,109.2]},"Salvador":{"label":"Salvador","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[3,0,0,7,0,3,5,4,4,3,6,2,0,0,0,0],"anom":[0.28,-0.42,0.07,0.09,-0.68,0.16,0.42,0.03,0.46,0.62,0.1,-0.35,-0.57,null,null,null],"oer":[1.04,null,null,0.97,null,1.098,0.991,0.924,0.941,1.063,1.102,1.048,null,null,null,null],"sig":[0.0,null,null,0.0,null,0.0,25.0,25.0,20.0,0.0,14.3,0.0,null,null,null,null],"obitos":[27.4,0,0,-16.9,0,28.6,-11.7,-54.6,-27.6,14.3,90.9,13.8,0,0,0,0]},"São Paulo":{"label":"São Paulo","years":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],"events":[4,3,7,4,7,4,4,2,3,7,2,1,6,6,11,4],"anom":[0.2,-0.01,0.71,-0.49,1.0,0.55,0.18,-0.05,0.16,0.95,-0.78,-0.2,0.08,1.26,1.96,0.81],"oer":[0.985,1.077,1.054,1.055,1.105,1.119,1.133,1.195,1.211,1.151,1.186,1.131,1.231,1.192,1.29,1.265],"sig":[28.6,75.0,25.0,33.3,71.4,71.4,71.4,100.0,100.0,90.9,66.7,50.0,100.0,85.7,100.0,100.0],"obitos":[-18.4,337.5,331.1,134.8,1229.8,923.2,919.0,547.6,870.9,1280.6,313.9,110.0,1959.5,1490.7,3585.7,2055.2]}};
    var ORDEM = Object.keys(CIDADES);

    function el(tag, attrs) {
      var e = document.createElementNS(NS, tag);
      for (var k in attrs) e.setAttribute(k, attrs[k]);
      return e;
    }
    function clear(svg) { while (svg.firstChild) svg.removeChild(svg.firstChild); }
    function fmtInt(v) { return Math.round(v).toLocaleString("pt-BR"); }
    function niceMax(v) {
      if (v <= 10) return Math.ceil(v / 2) * 2 + 2;
      var step = v <= 30 ? 5 : (v <= 80 ? 10 : 20);
      return Math.ceil(v / step) * step;
    }
    function range(vals, pad, includeZero, includeOne) {
      var xs = vals.filter(function (v) { return v !== null && v !== undefined; });
      if (!xs.length) return {min: 0, max: 1};
      var mn = Math.min.apply(null, xs), mx = Math.max.apply(null, xs);
      if (includeZero) { mn = Math.min(mn, 0); mx = Math.max(mx, 0); }
      if (includeOne) { mn = Math.min(mn, 1); mx = Math.max(mx, 1); }
      var span = (mx - mn) || 1;
      return {min: mn - span * pad, max: mx + span * pad};
    }

    function drawBar(svgId, data, years, opts) {
      var svg = document.getElementById(svgId);
      if (!svg) return;
      clear(svg);
      var W = 360, H = 190, padL = 26, padR = 6, padT = 12, padB = 22;
      var innerW = W - padL - padR, innerH = H - padT - padB;
      var minV = opts.min, maxV = opts.max, span = maxV - minV, n = data.length;
      var bw = innerW / n * 0.66, gap = innerW / n;
      function y(v) { return padT + innerH - ((v - minV) / span) * innerH; }
      function x(i) { return padL + gap * i + (gap - bw) / 2; }
      [minV, minV + span / 2, maxV].forEach(function (v) {
        var gy = y(v);
        svg.appendChild(el("line", {x1: padL, x2: W - padR, y1: gy, y2: gy,
          stroke: "#e9eef1", "stroke-width": 1}));
        var t = el("text", {x: padL - 4, y: gy + 3, "text-anchor": "end",
          "font-size": 8.5, fill: "#8098a6", "font-family": "Segoe UI, Arial, sans-serif"});
        t.textContent = opts.fmt(v);
        svg.appendChild(t);
      });
      if (opts.ref !== undefined && opts.ref !== null) {
        var ry = y(opts.ref);
        svg.appendChild(el("line", {x1: padL, x2: W - padR, y1: ry, y2: ry,
          stroke: "#8098a6", "stroke-width": 1, "stroke-dasharray": "3 3"}));
      }
      data.forEach(function (v, i) {
        var bx = x(i), by = y(v), bh = y(minV) - y(v);
        var hi = opts.highlight.indexOf(years[i]) !== -1;
        svg.appendChild(el("rect", {x: bx, y: by, width: bw, height: Math.max(bh, 0.5),
          fill: hi ? "#e63946" : "#2b9eb3", opacity: hi ? 1 : 0.55, rx: 1}));
        if (i === 0 || i === n - 1 || years[i] % 5 === 0) {
          var lbl = el("text", {x: bx + bw / 2, y: H - 6, "text-anchor": "middle",
            "font-size": 8.5, fill: "#8098a6", "font-family": "Segoe UI, Arial, sans-serif"});
          lbl.textContent = "'" + String(years[i]).slice(2);
          svg.appendChild(lbl);
        }
        if (hi) {
          var pl = el("text", {x: bx + bw / 2, y: by - 4, "text-anchor": "middle",
            "font-size": 10, fill: "#c22e3d", "font-weight": 700,
            "font-family": "Segoe UI, Arial, sans-serif"});
          pl.textContent = v;
          svg.appendChild(pl);
        }
      });
    }

    function drawLine(svgId, data, years, opts) {
      var svg = document.getElementById(svgId);
      if (!svg) return;
      clear(svg);
      var W = 360, H = 190, padL = 30, padR = 8, padT = 14, padB = 22;
      var innerW = W - padL - padR, innerH = H - padT - padB;
      var minV = opts.min, maxV = opts.max, span = maxV - minV, n = data.length;
      function y(v) { return padT + innerH - ((v - minV) / span) * innerH; }
      function x(i) { return padL + (innerW / (n - 1)) * i; }
      [minV, minV + span / 2, maxV].forEach(function (v) {
        var gy = y(v);
        svg.appendChild(el("line", {x1: padL, x2: W - padR, y1: gy, y2: gy,
          stroke: "#e9eef1", "stroke-width": 1}));
        var t = el("text", {x: padL - 4, y: gy + 3, "text-anchor": "end",
          "font-size": 8.5, fill: "#8098a6", "font-family": "Segoe UI, Arial, sans-serif"});
        t.textContent = opts.fmt(v);
        svg.appendChild(t);
      });
      if (opts.zeroLine) {
        var zy = y(0);
        svg.appendChild(el("line", {x1: padL, x2: W - padR, y1: zy, y2: zy,
          stroke: "#c7d3da", "stroke-width": 1}));
      }
      if (opts.refOne) {
        var oy = y(1);
        svg.appendChild(el("line", {x1: padL, x2: W - padR, y1: oy, y2: oy,
          stroke: "#8098a6", "stroke-width": 1, "stroke-dasharray": "3 3"}));
      }
      var d = "", started = false;
      data.forEach(function (v, i) {
        if (v === null || v === undefined) { started = false; return; }
        d += (started ? "L" : "M") + x(i).toFixed(1) + " " + y(v).toFixed(1) + " ";
        started = true;
      });
      if (d) svg.appendChild(el("path", {d: d.trim(), fill: "none", stroke: "#1761a0", "stroke-width": 2.2}));
      data.forEach(function (v, i) {
        if (v === null || v === undefined) return;
        var hi = opts.highlight.indexOf(years[i]) !== -1;
        svg.appendChild(el("circle", {cx: x(i), cy: y(v), r: hi ? 2.8 : 1.6,
          fill: hi ? "#e63946" : "#1761a0"}));
        if (i === 0 || i === n - 1 || years[i] % 5 === 0) {
          var lbl = el("text", {x: x(i), y: H - 6, "text-anchor": "middle",
            "font-size": 8.5, fill: "#8098a6", "font-family": "Segoe UI, Arial, sans-serif"});
          lbl.textContent = "'" + String(years[i]).slice(2);
          svg.appendChild(lbl);
        }
      });
    }

    function setStat(n, l, nVal, lVal) {
      document.getElementById(n).textContent = nVal;
      document.getElementById(l).textContent = lVal;
    }

    function highlightRows(key) {
      ["tbl-rm-body", "tbl-obitos-body"].forEach(function (tid) {
        var body = document.getElementById(tid);
        if (!body) return;
        Array.prototype.forEach.call(body.querySelectorAll("tr"), function (tr) {
          tr.classList.toggle("rm-hi", key !== "__GERAL__" && tr.getAttribute("data-city") === key);
        });
      });
    }

    function render(key) {
      var d = CIDADES[key];
      if (!d) return;
      var years = d.years, geral = key === "__GERAL__";

      var evR = range(d.events, 0.12, true, false);
      drawBar("chart-events", d.events, years, {
        min: 0, max: niceMax(evR.max), highlight: [2024],
        ref: d.events.slice(0, 14).reduce(function (a, b) { return a + b; }, 0) / 14,
        fmt: fmtInt
      });

      var anomR = range(d.anom, 0.15, true, false);
      drawLine("chart-anom", d.anom, years, {
        min: anomR.min, max: anomR.max, highlight: [2024], zeroLine: true,
        fmt: function (v) { return v.toFixed(1); }
      });

      var oerR = range(d.oer, 0.12, false, true);
      drawLine("chart-oer", d.oer, years, {
        min: oerR.min, max: oerR.max, highlight: [2025], refOne: true,
        fmt: function (v) { return v.toFixed(2); }
      });

      var sigR = range(d.sig, 0.1, true, false);
      drawLine("chart-sig", d.sig, years, {
        min: Math.max(0, sigR.min), max: Math.min(100, Math.max(sigR.max, 10)), highlight: [2025],
        fmt: function (v) { return Math.round(v) + "%"; }
      });

      var ev24 = d.events[14], ev25 = d.events[15];
      var baseAvg = d.events.slice(0, 14).reduce(function (a, b) { return a + b; }, 0) / 14;
      var deltaPct = baseAvg > 0 ? Math.round((ev24 / baseAvg - 1) * 100) : null;
      if (geral) {
        setStat("s1n", "s1l", ev24, "ondas de calor em 2024, recorde da s\u00e9rie 1981-2025 (" +
          (deltaPct >= 0 ? "+" : "") + deltaPct + "% vs. m\u00e9dia 2010-2023)");
      } else {
        setStat("s1n", "s1l", ev24, "ondas de calor em 2024 (m\u00e9dia 2010-2023: " +
          baseAvg.toFixed(1) + "/ano" + (deltaPct !== null ? ", " + (deltaPct >= 0 ? "+" : "") + deltaPct + "%" : "") + ")");
      }

      var oer25 = d.oer[15];
      setStat("s2n", "s2l", (oer25 !== null && oer25 !== undefined) ? oer25.toFixed(2).replace(".", ",") : "\u2014",
        geral ? "raz\u00e3o O/E m\u00e9dia em 2025, maior valor anual da s\u00e9rie" :
                ((oer25 !== null && oer25 !== undefined) ? "raz\u00e3o O/E m\u00e9dia em 2025" : "sem onda com O/E calcul\u00e1vel em 2025"));

      var sig25 = d.sig[15];
      setStat("s3n", "s3l", (sig25 !== null && sig25 !== undefined) ? (sig25.toFixed(1).replace(".", ",") + "%") : "\u2014",
        geral ? "das ondas de 2025 com excesso significativo (vs. 42,6% em 2010-2023)" :
                ((sig25 !== null && sig25 !== undefined) ? "das ondas de 2025 com excesso significativo" : "sem onda com signific\u00e2ncia calcul\u00e1vel em 2025"));

      var obTotal = (d.obitos[14] || 0) + (d.obitos[15] || 0);
      setStat("s4n", "s4l", (obTotal >= 0 ? "\u2248" : "\u2212\u2248") + fmtInt(Math.abs(obTotal)),
        geral ? "\u00f3bitos atribu\u00edveis a ondas de calor em 2024+2025 (2025 parcial)" :
                "\u00f3bitos atribu\u00edveis a ondas de calor em 2024+2025");

      var note = document.getElementById("rm-note");
      var notes = [];
      if (key === "Salvador") {
        notes.push("Sem temperatura v\u00e1lida desde janeiro de 2022 \u2014 os valores de 2022 em diante n\u00e3o s\u00e3o zero real, refletem aus\u00eancia de dado.");
      } else if (!geral && ev25 === 0 && ev24 > 0) {
        notes.push("Nenhum evento de onda de calor detectado em 2025 pelos crit\u00e9rios de EHF atuais.");
      }
      note.textContent = notes.join(" ");

      highlightRows(key);
    }

    var sel = document.getElementById("rm-select");
    ORDEM.forEach(function (key) {
      var opt = document.createElement("option");
      opt.value = key;
      opt.textContent = CIDADES[key].label;
      sel.appendChild(opt);
    });
    var recifeOpt = document.createElement("option");
    recifeOpt.value = "__RECIFE__";
    recifeOpt.disabled = true;
    recifeOpt.textContent = "Recife (sem dado clim\u00e1tico v\u00e1lido desde 2020)";
    sel.appendChild(recifeOpt);

    sel.addEventListener("change", function () { render(this.value); });
    render("__GERAL__");
  })();
  </script>
</body>
</html>"""
