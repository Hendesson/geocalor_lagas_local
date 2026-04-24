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
    .links-cell a::before { content: "🔗 "; font-size: 0.85em; }
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
    <button onclick="window.print()">🖨 Imprimir / Salvar como PDF</button>
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
    <button onclick="window.print()">🖨 Imprimir / Salvar como PDF</button>
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
      🖨 Imprimir / Salvar como PDF
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
  15 Regiões Metropolitanas do Brasil no período de <strong>1981 a 2023</strong>.</p>
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
      🖨 Imprimir / Salvar como PDF
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
    <li>Dados meteorológicos: INMET e ICEA (1981–2023).</li>
    <li>Regiões Metropolitanas: IBGE.</li>
  </ul>

  <p class="no-print" style="margin-top:2.5rem;">
    <button onclick="window.print()" style="padding:10px 24px; background:#1761a0;
      color:#fff; border:none; border-radius:6px; cursor:pointer; font-size:1rem;">
      🖨 Imprimir / Salvar como PDF
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
    hospitalares do SUS. Cobre o período de <strong>2010 a 2022</strong> para as Regiões
    Metropolitanas selecionadas. Cada registro corresponde a uma Autorização de Internação
    Hospitalar (AIH).</li>
    <li><strong>SIM — Sistema de Informações sobre Mortalidade:</strong> registros de óbitos
    ocorridos no território nacional. Cobre o período de <strong>2010 a 2023</strong>.
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
      🖨 Imprimir / Salvar como PDF
    </button>
  </p>
</body>
</html>"""
