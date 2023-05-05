class UnexpectedEventException(Exception):
    def __init__(self, expected_event_type: type):
        super().__init__(f"Unexpected event type received, expecting {expected_event_type.__name__}")
