from datetime import datetime, timezone

from babel.dates import format_date


class Utils:
    @staticmethod
    def current_utc_time() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def current_month() -> str:
        # Data atual
        data_atual = Utils.current_utc_time()

        return format_date(data_atual, "MMMM", locale="pt_BR")
