from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum


class Phase(str, Enum):
    MENSTRUACAO = "Menstruação"
    FOLICULAR = "Entre fases"
    OVULACAO = "Ovulação"
    TPM = "TPM / pré-menstrual"
    NAO_SEI = "Não sei"


@dataclass(frozen=True)
class CycleEstimate:
    cycle_day: int
    cycle_length: int
    period_length: int
    phase: Phase
    next_period: date
    days_to_next_period: int
    confidence: str
    explanation: str
    source: str


def _clamp_cycle(cycle_length: int, period_length: int) -> tuple[int, int]:
    return max(21, min(int(cycle_length), 45)), max(2, min(int(period_length), 10))


def phase_for_day(cycle_day: int, cycle_length: int = 28, period_length: int = 5) -> Phase:
    cycle_length, period_length = _clamp_cycle(cycle_length, period_length)
    cycle_day = max(1, min(int(cycle_day), cycle_length))
    ovulation_day = max(period_length + 3, cycle_length - 14)
    premenstrual_start = max(ovulation_day + 3, cycle_length - 5)

    if cycle_day <= period_length:
        return Phase.MENSTRUACAO
    if abs(cycle_day - ovulation_day) <= 2:
        return Phase.OVULACAO
    if cycle_day >= premenstrual_start:
        return Phase.TPM
    return Phase.FOLICULAR


def _anchor_day(phase: Phase, cycle_length: int, period_length: int) -> int:
    ovulation_day = max(period_length + 3, cycle_length - 14)
    if phase == Phase.MENSTRUACAO:
        return min(2, period_length)
    if phase == Phase.OVULACAO:
        return ovulation_day
    if phase == Phase.TPM:
        return max(ovulation_day + 3, cycle_length - 3)
    if phase == Phase.FOLICULAR:
        return min(cycle_length, max(period_length + 3, 8))
    return 1


def estimate_from_phase_date(
    phase: Phase,
    reference_date: date,
    cycle_length: int = 28,
    period_length: int = 5,
    today: date | None = None,
    source: str = "data informada",
) -> CycleEstimate:
    """Estima a posição no ciclo usando uma fase conhecida como âncora.

    É uma aproximação educacional. Fase pré-menstrual e ovulação variam entre
    ciclos e calendário isolado não confirma fertilidade.
    """
    today = today or date.today()
    cycle_length, period_length = _clamp_cycle(cycle_length, period_length)
    anchor = _anchor_day(phase, cycle_length, period_length)
    elapsed = (today - reference_date).days
    cycle_day = ((anchor - 1 + elapsed) % cycle_length) + 1
    current_phase = phase_for_day(cycle_day, cycle_length, period_length)
    days_to_next_period = cycle_length - cycle_day + 1
    next_period = today + timedelta(days=days_to_next_period)

    confidence = "moderada" if phase == Phase.MENSTRUACAO and source == "data informada" else "baixa"
    if source == "fase atual informada":
        confidence = "baixa"

    return CycleEstimate(
        cycle_day=cycle_day,
        cycle_length=cycle_length,
        period_length=period_length,
        phase=current_phase,
        next_period=next_period,
        days_to_next_period=days_to_next_period,
        confidence=confidence,
        explanation=(
            "Estimativa de calendário. O ciclo real pode adiantar, atrasar ou não seguir este padrão. "
            "Use como contexto para conversar melhor, não como confirmação biológica."
        ),
        source=source,
    )


def estimate_from_current_phase(
    phase: Phase,
    cycle_length: int = 28,
    period_length: int = 5,
    today: date | None = None,
) -> CycleEstimate:
    today = today or date.today()
    return estimate_from_phase_date(
        phase=phase,
        reference_date=today,
        cycle_length=cycle_length,
        period_length=period_length,
        today=today,
        source="fase atual informada",
    )


def cycle_categories(cycle_length: int = 28, period_length: int = 5) -> list[Phase]:
    cycle_length, period_length = _clamp_cycle(cycle_length, period_length)
    return [phase_for_day(day, cycle_length, period_length) for day in range(1, cycle_length + 1)]
