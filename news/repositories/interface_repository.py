from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class RepositoryInterface(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def update(self, item, data):
        pass

    @abstractmethod
    def delete(self, item):
        pass

    @abstractmethod
    def create(self, item):
        pass
