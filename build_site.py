"""Gera index.html autossuficiente (funciona offline) a partir de painel.html + dados/*.csv.
Uso: python3 build_site.py"""
import csv, json, pathlib, datetime

base = pathlib.Path(__file__).parent
painel = (base / "painel.html").read_text(encoding="utf-8")
d3 = (base / "vendor" / "d3.min.js").read_text(encoding="utf-8")
dados = {n: list(csv.DictReader(open(base / "dados" / f"{n}.csv", encoding="utf-8")))
         for n in ("variacao_mensal", "variacao_anual", "classes")}

style = painel[painel.index("<style>"):painel.index("</style>") + 8]
corpo = painel[painel.index('<div class="nf">'):painel.index("<script>")]
script = painel[painel.index("<script>"):painel.rindex("</script>") + 9]

tokens = """
:root { --font-anthropic-sans: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; --font-anthropic-serif: Georgia, "Times New Roman", serif;
  --cds-font-size-caption: 12px; --cds-font-size-body: 14px; --cds-font-size-heading: 16px; --cds-font-size-title: 22px; --cds-font-weight-medium: 500;
  --cds-gap-xs: 4px; --cds-gap-sm: 8px; --cds-gap-md: 12px; --cds-gap-lg: 16px; --cds-gap-xl: 24px;
  --cds-pad-xs: 4px; --cds-pad-sm: 8px; --cds-pad-md: 12px; --cds-pad-lg: 16px; --cds-pad-xl: 24px; --cds-radius: 8px; --cds-dur-slow: .3s;
  --color-bg: #f6f6f3; --color-panel: #ffffff; --color-fg: #1f1f1e; --color-fg-muted: #6b6a65; --color-border-line: #e3e2dc;
  --color-ok: #2e7d32; --color-bad: #b3261e; --cds-chart-grid: #ecebe6; --cds-chart-axis: #b9b8b1; --cds-chart-reference: #9c9b94; --cds-chart-status-critical: #c8463d;
  --cds-surface-popover: #ffffff; --cds-border: #e3e2dc; --cds-shadow-popover: 0 4px 16px rgba(0,0,0,.12); --cds-text-secondary: #6b6a65;
  --serie-1: #2f6fd0; --serie-2: #d9822b; color-scheme: light; }
@media (prefers-color-scheme: dark) { :root { --color-bg: #1a1a19; --color-panel: #242423; --color-fg: #ecebe6; --color-fg-muted: #a3a29b; --color-border-line: #3a3a37;
  --color-ok: #7cc47f; --color-bad: #f28b82; --cds-chart-grid: #333331; --cds-chart-axis: #5a5955; --cds-chart-reference: #7d7c76; --cds-chart-status-critical: #f0776c;
  --cds-surface-popover: #2c2c2a; --cds-border: #3a3a37; --cds-shadow-popover: 0 4px 16px rgba(0,0,0,.5); --cds-text-secondary: #a3a29b;
  --serie-1: #6aa0ec; --serie-2: #eba25a; color-scheme: dark; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--color-bg); color: var(--color-fg); font-family: var(--font-anthropic-sans); font-size: 14px; }
#dash-root { padding: clamp(16px, 3vw, 32px); max-width: 1500px; margin-inline: auto; }
.nf-atualizado { font-size: 12px; color: var(--color-fg-muted); margin: 0; }
"""

# substitui o runtime do claude.ai por uma versão local com os dados embutidos
runtime = """<script>
(function () {
  const DADOS = %s, CALC = {}, cbs = [];
  window.dash = {
    colors: ['var(--serie-1)', 'var(--serie-2)'],
    calc: (id, o) => { CALC[id] = o; },
    data: (id) => {
      if (DADOS[id]) return { status: 'ok', data: DADOS[id] };
      const o = CALC[id];
      if (!o) return { status: 'missing', data: [] };
      return { status: 'ok', data: o.fn(...o.inputs.map(i => window.dash.data(i).data)) };
    },
    onData: (fn) => { cbs.push(fn); fn(); }
  };
  let t; addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => cbs.forEach(f => f()), 150); });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => cbs.forEach(f => f()));
})();
</script>""" % json.dumps(dados, ensure_ascii=False)

hoje = datetime.date.today().strftime("%d/%m/%Y")
html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Monitor de Vendas NFC-e · Fecomércio-RS</title>
<meta name="description" content="Variação mensal das vendas registradas em NFC-e no varejo do Rio Grande do Sul, por classe da CNAE 2.0.">
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#1e3559">
<style>{tokens}</style>
{style}
</head>
<body>
<div id="dash-root">
{corpo}
<p class="nf-atualizado">Página gerada em {hoje}. Fonte: SEFAZ-RS, elaboração Fecomércio-RS.</p>
</div>
<script>{d3}</script>
{runtime}
{script}
<script>
if ('serviceWorker' in navigator && location.protocol.startsWith('http')) navigator.serviceWorker.register('sw.js');
</script>
</body>
</html>
"""
(base / "index.html").write_text(html, encoding="utf-8")
print("index.html gerado:", len(html.encode()) // 1024, "KB")
