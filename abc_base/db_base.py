from abc import ABCMeta, abstractmethod


# DbBase is set metaclass=ABCMeta,
# so all @abstractmethod defined in class should be implemented in all DbBase's descendant classes
class DbBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, file_name):
        pass

    @staticmethod
    @abstractmethod
    def get_pending_queue():
        pass

    @staticmethod
    @abstractmethod
    def is_page_in_queue():
        pass

    @staticmethod
    @abstractmethod
    def save_pending_queue():
        pass

    @staticmethod
    @abstractmethod
    def set_page_crawled():
        pass
