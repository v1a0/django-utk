from abc import ABC, abstractmethod


class DataFactory(ABC):

    @abstractmethod
    def getter(self, *args, **kwargs):
        raise NotImplemented

    def __call__(self, **kwargs):
        kwargs = {**self.kwargs, **kwargs}
        return self.getter(*self.args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
