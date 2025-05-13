class EventError(Exception):
    """Exception base class for event-related errors."""

class EventNotRegisteredError(EventError):
    """Raised when it is tried to dispatch an event that was not yet registered."""

    def __init__(self, signal: str) -> None:
        self.signal = signal
        super().__init__(f"Signal '{signal}' has no designated listeners.")

class EventExecutionError(EventError):
    """Raised when an error occured while trying to execute an event listener."""

    def __init__(self, error: Exception, signal: str) -> None:
        self.error = error
        self.signal = signal
        super().__init__(f"An error occured while dispatching to signal '{signal}': {error}")