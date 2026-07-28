from titan.core.investigation import Investigation, InvestigationReopened


def test_reopen_records_investigation_reopened_event() -> None:
    investigation = Investigation.create(
        title="NVIDIA Long-Term",
        purpose="Evaluate long-term investment thesis.",
    )

    investigation.close()
    investigation.pull_events()

    investigation.reopen()

    events = investigation.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], InvestigationReopened)
