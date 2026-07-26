class Entity[EventT]:
    def __init__(self) -> None:
        self._events: list[EventT] = []

    def pull_events(self) -> list[EventT]:
        events = self._events.copy()
        self._events.clear()
        return events

    def _record_event(self, event: EventT) -> None:
        self._events.append(event)
