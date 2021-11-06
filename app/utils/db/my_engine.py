from datetime import datetime

from odmantic import AIOEngine
from odmantic.engine import ModelType


class MyAIOEngine(AIOEngine):
    async def save(self, instance: ModelType) -> ModelType:
        if hasattr(instance, 'updated_at'):
            instance.updated_at = datetime.now()
        return await super().save(instance)
