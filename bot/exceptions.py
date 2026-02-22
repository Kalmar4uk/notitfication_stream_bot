class NotValidСredentials(Exception):
    """Ошибки при получении токена"""
    def __init__(self, error: str | None = None):
        self.error = error
        super().__init__(self.error)


class NotStreamNow(Exception):
    """Ошибка отсутствия стрима"""
    def __init__(self, error: str = "На текущий момент нет активного стрима"):
        self.error = error
        super().__init__(self.error)
