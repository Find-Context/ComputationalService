from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, entity):
        pass

    @abstractmethod
    async def get_by_id(self, id: int):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def update(self, entity):
        pass

    @abstractmethod
    async def delete(self, id: int):
        pass
