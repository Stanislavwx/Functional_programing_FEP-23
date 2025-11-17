from __future__ import annotations

from decorators import retries


def test_retries_succeeds_on_third_attempt() -> None:
    calls = {"n": 0, "slept": []}
    def fake_sleep(t: float) -> None:
        calls["slept"].append(t)

    @retries(attempts=3, delay=0.0, backoff=1.0, jitter=0.0, sleep=fake_sleep, logger=lambda s: None)
    def flaky() -> str:
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("boom")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3
    # дві затримки між спробами
    assert len(calls["slept"]) == 2


def test_retries_raises_after_attempts() -> None:
    calls = {"n": 0}
    @retries(attempts=2, delay=0.0, backoff=1.0, jitter=0.0, sleep=lambda _: None, logger=lambda s: None)
    def always_fail() -> None:
        calls["n"] += 1
        raise ValueError("nope")

    try:
        always_fail()
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"
    assert calls["n"] == 2
