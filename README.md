# Monitor de Vendas por NFC-e · Varejo RS

Painel da Fecomércio-RS com a variação mensal do valor vendido em NFC-e no varejo do Rio Grande do Sul, por classe da CNAE 2.0 (fonte: SEFAZ-RS).

**Acesse:** https://pietrosalvador5-boop.github.io/monitor-nfce-varejo/

## Usar sem internet
- Depois de abrir o site uma vez, o navegador guarda uma cópia e ele abre mesmo offline.
- Ou baixe o `index.html` e abra direto no navegador: dados e gráficos estão todos dentro do arquivo.

## Atualizar os dados
1. Substitua os arquivos em `dados/` (`variacao_mensal.csv`, `variacao_anual.csv`, `classes.csv`).
2. Rode `python3 build_site.py` para gerar o novo `index.html`.
3. Faça commit e push.

## Arquivos
- `painel.html`: layout do painel (estilos, estrutura e gráficos).
- `dados/`: dados em CSV, um registro por classe e mês.
- `build_site.py`: junta layout, dados e a biblioteca d3 num `index.html` único.
- `sw.js` e `manifest.webmanifest`: cópia offline do site no navegador.
