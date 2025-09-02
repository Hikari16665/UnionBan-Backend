class VerifyingUtils:
    @classmethod
    async def not_none(cls, *args) -> None:
        for arg in args:
            if arg is None:
                raise ValueError(f'Argument cannot be None')
        return