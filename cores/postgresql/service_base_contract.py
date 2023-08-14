from abc import ABCMeta, abstractmethod
from cores.schemas.sche_base import PaginationParams, MetadataSchema
class ServiceBaseContract:
    @abstractmethod
    def paginate(self, pagination_params: PaginationParams, query: dict = {}, sort_by: str = None, direction: str = None):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def create(self, data: object, with_timestamp=True) -> dict:
        pass

    @abstractmethod
    def find(self, id: str) -> dict:
        pass

    @abstractmethod
    def search(self, name: str, is_absolute: bool = True, is_get_first: bool = True):
        pass

    @abstractmethod
    def update(self, id: str, data: object) -> dict:
        pass

    @abstractmethod
    def delete(self, id: str, is_hard_delete=False) -> bool:
        pass

    @abstractmethod
    def set_table(self, table):
        pass