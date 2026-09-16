from __future__ import annotations

import html
import math
from typing import Iterable

import streamlit as st
import streamlit.components.v1 as components

from .domain import CycleEstimate, Phase, cycle_categories


APP_CSS = r"""
<style>
:root {
  --bg:#F7F3ED;
  --surface:#FFFDF9;
  --ink:#1D2723;
  --muted:#6E7772;
  --line:rgba(29,39,35,.10);
  --green:#355D50;
  --green-soft:#E4EEE9;
  --rose:#C97E72;
  --rose-soft:#F4E3DF;
  --gold:#D7A85A;
  --gold-soft:#F5EBD8;
  --violet:#8B7BA8;
  --violet-soft:#ECE8F2;
  --neutral:#D8D5CE;
}

html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
html, body, #root { margin:0 !important; padding:0 !important; }
.stApp { background:var(--bg); color:var(--ink); min-height:100dvh; }

/* Remove de forma robusta o chrome do Streamlit e o espaço reservado no topo. */
header[data-testid="stHeader"],
[data-testid="stHeader"],
[data-testid="stAppHeader"],
.stAppHeader,
.stAppToolbar,
[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stAppDeployButton"],
.stDeployButton,
[class*="viewerBadge"],
[class*="ViewerBadge"],
[data-testid*="viewerBadge"],
#MainMenu,
footer {
  display:none !important;
  visibility:hidden !important;
  height:0 !important;
  min-height:0 !important;
  max-height:0 !important;
  padding:0 !important;
  margin:0 !important;
}

header[data-testid="stHeader"],
[data-testid="stHeader"],
[data-testid="stAppHeader"],
.stAppHeader {
  position:absolute !important;
  inset:0 auto auto 0 !important;
  width:0 !important;
  overflow:hidden !important;
  opacity:0 !important;
  pointer-events:none !important;
  border:0 !important;
  box-shadow:none !important;
  background:transparent !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.stMain,
.main {
  margin-top:0 !important;
  padding-top:0 !important;
  top:0 !important;
  background:var(--bg) !important;
}

[data-testid="stAppViewContainer"] > .main,
[data-testid="stMain"] > div,
section.main {
  padding-top:0 !important;
  margin-top:0 !important;
}

/* Streamlit 1.5x/1.6x usa stMainBlockContainer e aplica 6rem em apps não embedded. */
[data-testid="stMainBlockContainer"],
.stMainBlockContainer,
.stAppViewBlockContainer,
.main .block-container,
.block-container {
  max-width:560px;
  padding-top:max(.45rem, env(safe-area-inset-top)) !important;
  margin-top:0 !important;
  padding-right:1rem !important;
  padding-bottom:5rem !important;
  padding-left:1rem !important;
  margin-top:0 !important;
}

[data-testid="stSidebar"] { display:none !important; }

h1,h2,h3,p { color:var(--ink); }
h1,h2,h3 { letter-spacing:-.035em; }
h1 { font-size:2.18rem !important; line-height:1.02 !important; margin:.25rem 0 .55rem !important; }
h2 { font-size:1.35rem !important; margin:1.35rem 0 .55rem !important; }
p { line-height:1.55; }

.cc-top { display:flex; justify-content:space-between; align-items:center; margin:.1rem 0 1rem; }
.cc-brand { display:flex; align-items:center; gap:.58rem; font-weight:850; letter-spacing:-.02em; }
.cc-mark { width:34px; height:34px; border-radius:13px; display:grid; place-items:center; background:var(--green); color:white; font-size:1rem; }
.cc-private { font-size:.72rem; color:var(--muted); background:rgba(255,255,255,.65); border:1px solid var(--line); border-radius:999px; padding:.36rem .55rem; }

.cc-welcome { padding:1rem .1rem .45rem; }
.cc-kicker { color:var(--green); font-size:.76rem; text-transform:uppercase; letter-spacing:.08em; font-weight:850; }
.cc-welcome p { color:var(--muted); margin:.25rem 0 1rem; font-size:1rem; }
.cc-mini { color:var(--muted); font-size:.78rem; text-align:center; margin:.6rem 0; }

div.stButton > button, div.stFormSubmitButton > button {
  min-height:3.1rem; border-radius:16px; font-weight:800; border:1px solid var(--line);
  box-shadow:none; transition:.12s ease; width:100%;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover { transform:translateY(-1px); border-color:rgba(53,93,80,.35); }
div.stButton > button[kind="primary"], div.stFormSubmitButton > button[kind="primary"] { background:var(--green); color:#fff; border-color:var(--green); }

.cc-question { margin:.2rem 0 .85rem; }
.cc-question h1 { font-size:1.85rem !important; }
.cc-question p { color:var(--muted); margin:.25rem 0 0; }

.cc-option-note { color:var(--muted); font-size:.79rem; margin:-.22rem 0 .45rem; }

.cc-flower-card { background:linear-gradient(145deg,#FFFDF9,#F2ECE2); border:1px solid var(--line); border-radius:28px; padding:1.15rem 1.15rem 1rem; margin:.15rem 0 .8rem; overflow:hidden; position:relative; }
.cc-flower-card:after { content:"✿"; position:absolute; right:-.2rem; top:-1.2rem; font-size:7rem; color:rgba(201,126,114,.09); transform:rotate(14deg); }
.cc-flower-line { color:var(--muted); font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; font-weight:850; }
.cc-flower-name { font-size:2rem; line-height:1; font-weight:880; letter-spacing:-.05em; margin:.35rem 0 .45rem; }
.cc-status { display:inline-flex; align-items:center; gap:.42rem; background:var(--green-soft); color:#294A40; border-radius:999px; padding:.42rem .65rem; font-size:.79rem; font-weight:820; }
.cc-dot { width:7px; height:7px; border-radius:50%; background:var(--green); }

.cc-cycle-card { background:var(--surface); border:1px solid var(--line); border-radius:28px; padding:1rem .85rem .9rem; margin:.7rem 0; }
.cc-cycle-title { font-size:.82rem; font-weight:850; text-align:center; margin:.1rem 0 .6rem; }
.cc-cycle-wrap { display:grid; place-items:center; margin:.15rem 0 .55rem; }
.cc-cycle-meta { text-align:center; margin-top:-8.2rem; margin-bottom:5.7rem; pointer-events:none; }
.cc-cycle-meta .day { font-size:1.75rem; font-weight:900; letter-spacing:-.05em; }
.cc-cycle-meta .label { color:var(--muted); font-size:.72rem; margin-top:.15rem; }
.cc-legend { display:flex; justify-content:center; flex-wrap:wrap; gap:.35rem .65rem; margin:.4rem 0 .2rem; }
.cc-legend span { font-size:.69rem; color:var(--muted); display:inline-flex; align-items:center; gap:.28rem; }
.cc-legend i { width:7px; height:7px; border-radius:50%; display:inline-block; }

.cc-hint { color:var(--muted); font-size:.77rem; text-align:center; margin:.55rem 0 .4rem; }

.cc-detail { background:var(--surface); border:1px solid var(--line); border-radius:26px; padding:1.05rem; margin:.8rem 0; }
.cc-detail-top { display:flex; align-items:center; gap:.7rem; margin-bottom:.8rem; }
.cc-detail-icon { width:42px; height:42px; border-radius:14px; display:grid; place-items:center; background:var(--rose-soft); color:#8A5047; font-weight:900; }
.cc-detail-label { color:var(--muted); font-size:.68rem; text-transform:uppercase; letter-spacing:.075em; font-weight:850; }
.cc-detail h2 { margin:.05rem 0 0 !important; font-size:1.22rem !important; }
.cc-feel { background:var(--gold-soft); border-radius:19px; padding:.9rem; margin:.4rem 0 .8rem; }
.cc-feel .label { color:#87652F; font-size:.68rem; text-transform:uppercase; letter-spacing:.07em; font-weight:900; margin-bottom:.3rem; }
.cc-feel p { margin:0; font-size:.94rem; line-height:1.5; }
.cc-small-head { font-size:.8rem; font-weight:900; margin:.8rem 0 .3rem; }
.cc-list { margin:0; padding:0; list-style:none; }
.cc-list li { display:flex; gap:.5rem; align-items:flex-start; padding:.33rem 0; color:#4F5A55; font-size:.86rem; line-height:1.45; }
.cc-list li:before { content:"•"; color:var(--green); font-weight:900; }
.cc-list.avoid li:before { color:var(--rose); }
.cc-say { background:var(--green); color:white; border-radius:20px 20px 20px 7px; padding:.85rem .95rem; margin:.8rem 0 0; }
.cc-say .label { color:#BFD0C9; font-size:.66rem; text-transform:uppercase; letter-spacing:.07em; font-weight:900; }
.cc-say .text { color:white; font-size:.93rem; font-weight:720; line-height:1.45; margin-top:.25rem; }

.cc-tip { background:var(--surface); border:1px solid var(--line); border-radius:20px; padding:.9rem; margin:.55rem 0; }
.cc-tip strong { display:block; margin-bottom:.25rem; }
.cc-tip p { color:var(--muted); font-size:.86rem; margin:0; }
.cc-caution { background:var(--rose-soft); color:#68453E; border-radius:18px; padding:.82rem .9rem; font-size:.82rem; line-height:1.5; margin:.8rem 0; }
.cc-info { color:var(--muted); font-size:.76rem; line-height:1.5; margin:.7rem 0; }

[data-testid="stDateInput"], [data-testid="stSelectbox"], [data-testid="stSlider"] { margin-bottom:.45rem; }
[data-testid="stExpander"] { background:rgba(255,255,255,.55); border:1px solid var(--line); border-radius:16px; }

@media (max-width: 520px) {
  [data-testid="stMainBlockContainer"],
  .stMainBlockContainer,
  .stAppViewBlockContainer,
  .main .block-container,
  .block-container {
    padding-top:max(.35rem, env(safe-area-inset-top)) !important;
    padding-right:.82rem !important;
    padding-bottom:4rem !important;
    padding-left:.82rem !important;
  }
  h1 { font-size:1.95rem !important; }
  .cc-top { margin-top:0 !important; }
  .cc-cycle-card { padding:.9rem .55rem .8rem; }
}
</style>
"""


COLORS = {
    Phase.MENSTRUACAO: "#C97E72",
    Phase.FOLICULAR: "#8FAE9F",
    Phase.OVULACAO: "#D7A85A",
    Phase.TPM: "#8B7BA8",
}


def inject_css() -> None:
    # st.html is preferable for pure CSS and avoids a markdown wrapper.
    st.html(APP_CSS)


def force_mobile_shell_fix() -> None:
    """Persist the mobile shell fix in the parent document.

    Streamlit's React/Emotion layer can recreate the header and block-container
    after reruns. A zero-height component mirrors the CSS into <head> and
    reapplies the critical properties whenever the DOM changes.
    """
    components.html(
        r"""
<script>
(() => {
  const d = window.parent.document;
  const STYLE_ID = 'selene-mobile-shell-fix-v5';
  let style = d.getElementById(STYLE_ID);
  if (!style) {
    style = d.createElement('style');
    style.id = STYLE_ID;
    d.head.appendChild(style);
  }
  style.textContent = `
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    [data-testid="stAppHeader"],
    .stAppHeader,
    [data-testid="stToolbar"],
    .stAppToolbar,
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stAppDeployButton"] {
      display:none !important;
      visibility:hidden !important;
      height:0 !important; min-height:0 !important; max-height:0 !important;
      padding:0 !important; margin:0 !important;
      overflow:hidden !important; opacity:0 !important; pointer-events:none !important;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"], .stMain {
      top:0 !important; margin-top:0 !important; padding-top:0 !important;
      background:#F7F3ED !important;
    }
    [data-testid="stMainBlockContainer"],
    .stMainBlockContainer, .stAppViewBlockContainer, .block-container {
      padding-top:max(.35rem, env(safe-area-inset-top)) !important;
      margin-top:0 !important;
    }
    @media (max-width: 768px) {
      [data-testid="stMainBlockContainer"],
      .stMainBlockContainer, .stAppViewBlockContainer, .block-container {
        padding-top:max(.25rem, env(safe-area-inset-top)) !important;
      }
    }
  `;

  const fix = () => {
    d.querySelectorAll('header[data-testid="stHeader"], [data-testid="stHeader"], [data-testid="stAppHeader"], .stAppHeader').forEach(el => {
      el.style.setProperty('display', 'none', 'important');
      el.style.setProperty('height', '0', 'important');
      el.style.setProperty('min-height', '0', 'important');
      el.style.setProperty('max-height', '0', 'important');
      el.style.setProperty('padding', '0', 'important');
      el.style.setProperty('margin', '0', 'important');
      el.style.setProperty('pointer-events', 'none', 'important');
    });
    d.querySelectorAll('[data-testid="stMainBlockContainer"], .stMainBlockContainer, .stAppViewBlockContainer, .block-container').forEach(el => {
      el.style.setProperty('padding-top', 'max(.25rem, env(safe-area-inset-top))', 'important');
      el.style.setProperty('margin-top', '0', 'important');
    });
  };

  fix();
  if (!window.parent.__seleneShellObserver) {
    const obs = new MutationObserver(() => requestAnimationFrame(fix));
    obs.observe(d.body, {childList:true, subtree:true});
    window.parent.__seleneShellObserver = obs;
  }
  window.parent.addEventListener('resize', fix, {passive:true});
})();
</script>
        """,
        height=0,
        width=0,
        scrolling=False,
    )


def topbar() -> None:
    st.markdown(
        '<div class="cc-top"><div class="cc-brand"><span class="cc-mark">◌</span>Ciclo Claro</div><div class="cc-private">sessão privada</div></div>',
        unsafe_allow_html=True,
    )


def welcome() -> None:
    st.markdown(
        """
        <section class="cc-welcome">
          <div class="cc-kicker">entenda melhor. presuma menos.</div>
          <h1>Um pouco de contexto muda tudo.</h1>
          <p>Descubra em poucos toques onde ela pode estar no ciclo e como agir com mais atenção.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def question(title: str, body: str) -> None:
    st.markdown(
        f'<div class="cc-question"><h1>{html.escape(title)}</h1><p>{html.escape(body)}</p></div>',
        unsafe_allow_html=True,
    )


def flower_card(name: str, estimate: CycleEstimate) -> None:
    phase_name = estimate.phase.value
    st.markdown(
        f"""
        <section class="cc-flower-card">
          <div class="cc-flower-line">apelido desta sessão</div>
          <div class="cc-flower-name">{html.escape(name)}</div>
          <div class="cc-status"><span class="cc-dot"></span> Provavelmente: {html.escape(phase_name)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def cycle_ring(estimate: CycleEstimate) -> None:
    categories = cycle_categories(estimate.cycle_length, estimate.period_length)
    cx, cy, radius = 110, 110, 82
    dots = []
    for idx, phase in enumerate(categories, start=1):
        angle = (2 * math.pi * (idx - 1) / estimate.cycle_length) - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        active = idx == estimate.cycle_day
        r = 6.8 if active else 4.25
        stroke = '#1D2723' if active else 'none'
        sw = 2.2 if active else 0
        dots.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{COLORS[phase]}" stroke="{stroke}" stroke-width="{sw}" />'
        )
    svg = (
        '<svg width="220" height="220" viewBox="0 0 220 220" role="img" aria-label="Estimativa visual do ciclo">'
        + ''.join(dots)
        + f'<text x="110" y="105" text-anchor="middle" fill="#1D2723" font-size="27" font-weight="850">~ dia {estimate.cycle_day}</text>'
        + f'<text x="110" y="126" text-anchor="middle" fill="#6E7772" font-size="11">de {estimate.cycle_length} dias</text>'
        + '</svg>'
    )
    legend = ''.join(
        f'<span><i style="background:{color}"></i>{label}</span>'
        for label, color in [
            ('Menstruação', COLORS[Phase.MENSTRUACAO]),
            ('Entre fases', COLORS[Phase.FOLICULAR]),
            ('Ovulação', COLORS[Phase.OVULACAO]),
            ('TPM', COLORS[Phase.TPM]),
        ]
    )
    st.markdown(
        f"""
        <section class="cc-cycle-card">
          <div class="cc-cycle-title">Estimativa do ciclo</div>
          <div class="cc-cycle-wrap">{svg}</div>
          <div class="cc-legend">{legend}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def phase_detail(content: dict[str, object]) -> None:
    def items(values: Iterable[str], cls: str = '') -> str:
        return '<ul class="cc-list ' + cls + '">' + ''.join(f'<li>{html.escape(v)}</li>' for v in values) + '</ul>'

    st.markdown(
        f"""
        <section class="cc-detail">
          <div class="cc-detail-top">
            <div class="cc-detail-icon">{html.escape(str(content['icon']))}</div>
            <div><div class="cc-detail-label">entenda esta fase</div><h2>{html.escape(str(content['headline']))}</h2></div>
          </div>
          <div class="cc-feel"><div class="label">O que ela pode estar sentindo</div><p>{html.escape(str(content['feel']))}</p></div>
          <div class="cc-small-head">Como agir</div>
          {items(content['do'])}
          <div class="cc-small-head">Melhor evitar</div>
          {items(content['avoid'], 'avoid')}
          <div class="cc-say"><div class="label">Se quiser dizer algo</div><div class="text">“{html.escape(str(content['say']))}”</div></div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def tip_card(title: str, body: str) -> None:
    st.markdown(
        f'<div class="cc-tip"><strong>{html.escape(title)}</strong><p>{html.escape(body)}</p></div>',
        unsafe_allow_html=True,
    )


def caution(text: str) -> None:
    st.markdown(f'<div class="cc-caution">{html.escape(text)}</div>', unsafe_allow_html=True)


def info(text: str) -> None:
    st.markdown(f'<div class="cc-info">{html.escape(text)}</div>', unsafe_allow_html=True)
