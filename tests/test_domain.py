from datetime import date

from ciclo_claro.domain import Phase, estimate_from_current_phase, estimate_from_phase_date, phase_for_day


def test_phase_for_day_28_day_cycle():
    assert phase_for_day(2, 28, 5) == Phase.MENSTRUACAO
    assert phase_for_day(10, 28, 5) == Phase.FOLICULAR
    assert phase_for_day(14, 28, 5) == Phase.OVULACAO
    assert phase_for_day(26, 28, 5) == Phase.TPM


def test_exact_menstruation_date_is_useful_anchor():
    result = estimate_from_phase_date(
        Phase.MENSTRUACAO,
        date(2026, 9, 1),
        cycle_length=28,
        period_length=5,
        today=date(2026, 9, 15),
    )
    assert result.cycle_day == 16
    assert result.confidence == "moderada"


def test_current_phase_is_marked_low_confidence():
    result = estimate_from_current_phase(
        Phase.TPM,
        cycle_length=28,
        period_length=5,
        today=date(2026, 9, 15),
    )
    assert result.phase == Phase.TPM
    assert result.confidence == "baixa"
