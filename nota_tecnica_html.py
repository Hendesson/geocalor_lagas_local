"""HTML estático das notas técnicas (impressão/PDF) — mesmo conteúdo dos dashboards separados."""

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

  <h2>6. Limitações</h2>
  <ul>
    <li>O SIH cobre apenas internações do SUS (aproximadamente 75% das internações totais
    no Brasil); internações em serviços privados não estão incluídas.</li>
    <li>Possíveis inconsistências de codificação CID-10 entre municípios e ao longo do tempo.</li>
    <li>Dados de raça/cor e estado civil podem apresentar subnotificação ou inconsistência
    em alguns municípios.</li>
    <li>As taxas populacionais utilizam estimativas do IBGE, que podem divergir da
    população real em anos intercensitários.</li>
    <li>O SIM de 2023 pode estar sujeito a revisões posteriores pelo DATASUS.</li>
  </ul>

  <h2>7. Referências</h2>
  <ul>
    <li>DATASUS. Sistema de Informações Hospitalares do SUS (SIH/SUS).
    Ministério da Saúde, Brasil.</li>
    <li>DATASUS. Sistema de Informações sobre Mortalidade (SIM).
    Ministério da Saúde, Brasil.</li>
    <li>IBGE. Estimativas de população. Instituto Brasileiro de Geografia e Estatística.</li>
    <li>Organização Mundial da Saúde. CID-10 — Classificação Estatística Internacional
    de Doenças e Problemas Relacionados à Saúde. 10ª rev. Genebra: OMS.</li>
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
