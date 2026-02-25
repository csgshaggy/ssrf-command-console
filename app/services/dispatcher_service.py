# app/services/dispatcher_service.py

from dispatcher import Dispatcher


class DispatcherService:
    """
    Thin wrapper around the global Dispatcher instance.
    Keeps dispatcher logic in the service layer.
    """

    def __init__(self):
        self._dispatcher = Dispatcher()

    def list_modes(self):
        return self._dispatcher.list_modes()

    def run_mode(self, mode: str, target: str, options: dict):
        return self._dispatcher.run_mode(mode, target, options)


# Global service instance
dispatcher_service = DispatcherService()
