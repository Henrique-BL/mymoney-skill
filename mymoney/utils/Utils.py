from datetime import datetime, timezone


class Utils:
    @staticmethod
    def current_utc_time() -> datetime:
        return datetime.now(timezone.utc)
