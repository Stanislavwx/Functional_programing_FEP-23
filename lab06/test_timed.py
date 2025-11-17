from __future__ import annotations

from decorators import timed


def test_timed_uses_clock_and_logger() -> None:
    ticks = [0.0, 0.012345]  # 12.345 ms
    def fake_clock() -> float:
        return ticks.pop(0)
    logs: list[str] = []
    def fake_log(s: str) -> None:
        logs.append(s)

    @timed("work", unit="ms", logger=fake_log, clock=fake_clock)
    def work(x: int) -> int:
        """square"""
        return x * x

    assert work(5) == 25
    assert any("work took 12.345 ms" in m for m in logs)
    # wraps зберігає метадані
    assert work.__name__ == "work"
    assert "square" in (work.__doc__ or "")


def test_timed_logs_on_exception() -> None:
    ticks = [0.0, 0.001]
    def fake_clock() -> float: return ticks.pop(0)
    logs: list[str] = []
    def fake_log(s: str) -> None: logs.append(s)

    @timed(unit="ms", logger=fake_log, clock=fake_clock)
    def boom() -> None:
        raise RuntimeError("X")

    try:
        boom()
    except RuntimeError:
        pass
    else:
        assert False, "Expected RuntimeError"
    assert logs, "Log should be produced in finally-block"
