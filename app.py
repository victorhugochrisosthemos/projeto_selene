from __future__ import annotations

import random
from datetime import date

import streamlit as st

from ciclo_claro.content import FLOWER_NAMES, PHASE_CONTENT, UNKNOWN_AVOID, UNKNOWN_TIPS
from ciclo_claro.domain import Phase, estimate_from_current_phase, estimate_from_phase_date
from ciclo_claro.ui import (
    caution,
    cycle_ring,
    flower_card,
    info,
    inject_css,
    force_mobile_shell_fix,
    phase_detail,
    question,
    tip_card,
    topbar,
    welcome,
)


APP_NAME = "Selene"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="◌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_css()
force_mobile_shell_fix()


def init_state() -> None:
    defaults = {
        "screen": "welcome",
        "estimate": None,
        "flower": None,
        "detail_phase": None,
        "cycle_length": 28,
        "period_length": 5,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go(screen: str) -> None:
    st.session_state.screen = screen
    st.rerun()


def set_estimate(estimate) -> None:
    st.session_state.estimate = estimate
    if not st.session_state.flower:
        st.session_state.flower = random.choice(FLOWER_NAMES)
    st.session_state.detail_phase = estimate.phase
    st.session_state.screen = "dashboard"
    st.rerun()


def choose_current_phase(phase: Phase) -> None:
    set_estimate(
        estimate_from_current_phase(
            phase,
            cycle_length=st.session_state.cycle_length,
            period_length=st.session_state.period_length,
        )
    )


def render_welcome() -> None:
    topbar()
    welcome()
    if st.button("Começar", type="primary", use_container_width=True):
        go("setup")
    st.markdown('<div class="cc-mini">Sem cadastro. Nenhum nome é necessário.</div>', unsafe_allow_html=True)


def render_setup() -> None:
    topbar()
    question("O que você sabe agora?", "Escolha só uma opção. O restante é estimado.")

    if st.button("📅  Sei a data específica de uma fase", use_container_width=True):
        go("specific_date")
    if st.button("●  Menstruação", use_container_width=True):
        choose_current_phase(Phase.MENSTRUACAO)
    if st.button("◐  TPM", use_container_width=True):
        choose_current_phase(Phase.TPM)
    if st.button("◉  Ovulação", use_container_width=True):
        choose_current_phase(Phase.OVULACAO)
    if st.button("?  Não sei", use_container_width=True):
        go("unknown")

    info("Se você só sabe a fase de hoje, a posição no ciclo terá baixa precisão. Uma data conhecida melhora a estimativa.")


def render_specific_date() -> None:
    topbar()
    question("Qual fase e qual data?", "Use apenas algo que ela tenha compartilhado com você.")

    phase_label = st.selectbox("Fase conhecida", ["Menstruação", "TPM", "Ovulação"])
    reference_date = st.date_input(
        "Data em que ela estava nessa fase",
        value=date.today(),
        max_value=date.today(),
        format="DD/MM/YYYY",
    )

    with st.expander("Ajustar o ciclo, se você souber"):
        cycle_length = st.slider("Duração média do ciclo", 21, 45, st.session_state.cycle_length)
        period_length = st.slider("Duração média da menstruação", 2, 10, st.session_state.period_length)

    phase_map = {
        "Menstruação": Phase.MENSTRUACAO,
        "TPM": Phase.TPM,
        "Ovulação": Phase.OVULACAO,
    }

    if st.button("Criar estimativa", type="primary", use_container_width=True):
        st.session_state.cycle_length = cycle_length
        st.session_state.period_length = period_length
        set_estimate(
            estimate_from_phase_date(
                phase_map[phase_label],
                reference_date,
                cycle_length=cycle_length,
                period_length=period_length,
            )
        )

    if st.button("Voltar", use_container_width=True):
        go("setup")



def render_unknown() -> None:
    topbar()
    question("Não sabe a fase? Tudo bem.", "Você pode descobrir sem pressionar nem transformar comportamento em pista.")

    for title, body in UNKNOWN_TIPS:
        tip_card(title, body)
    caution(UNKNOWN_AVOID)

    if st.button("Já consegui uma informação", type="primary", use_container_width=True):
        go("setup")
    if st.button("Voltar", use_container_width=True):
        go("setup")


def phase_buttons() -> None:
    st.markdown('<div class="cc-hint">Toque em uma fase para entender o que pode acontecer</div>', unsafe_allow_html=True)
    row1 = st.columns(2, gap="small")
    row2 = st.columns(2, gap="small")
    buttons = [
        (row1[0], "● Menstruação", Phase.MENSTRUACAO),
        (row1[1], "○ Entre fases", Phase.FOLICULAR),
        (row2[0], "◉ Ovulação", Phase.OVULACAO),
        (row2[1], "◐ TPM", Phase.TPM),
    ]
    for container, label, phase in buttons:
        with container:
            if st.button(label, use_container_width=True, key=f"phase_{phase.name}"):
                st.session_state.detail_phase = phase
                st.rerun()


def render_dashboard() -> None:
    estimate = st.session_state.estimate
    if estimate is None:
        go("setup")
        return

    topbar()
    flower_card(st.session_state.flower or "Jasmim", estimate)
    cycle_ring(estimate)
    phase_buttons()

    selected = st.session_state.detail_phase or estimate.phase
    phase_detail(PHASE_CONTENT[selected])

    info(
        f"Estimativa {estimate.confidence}. {estimate.explanation} "
        "O app não deve ser usado para contracepção, diagnóstico ou confirmação de ovulação."
    )

    with st.expander("Privacidade e fontes"):
        st.write(
            "Nesta versão Streamlit Cloud, as escolhas e datas são processadas na sessão do servidor para gerar a tela, "
            "mas o app não grava esses dados em SQLite, arquivo ou histórico próprio. Ao encerrar a sessão, o contexto é descartado."
        )
        st.write(
            "Referências de saúde usadas no conteúdo: Organização Mundial da Saúde (Menstrual health) e ACOG "
            "(Premenstrual Syndrome; The Menstrual Cycle)."
        )

    if st.button("Refazer estimativa", use_container_width=True):
        st.session_state.estimate = None
        st.session_state.flower = None
        st.session_state.detail_phase = None
        go("setup")


init_state()

screens = {
    "welcome": render_welcome,
    "setup": render_setup,
    "specific_date": render_specific_date,
    "unknown": render_unknown,
    "dashboard": render_dashboard,
}

screens.get(st.session_state.screen, render_welcome)()
