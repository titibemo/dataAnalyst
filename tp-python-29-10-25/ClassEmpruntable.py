from abc import ABC, abstractmethod

class Empruntable(ABC):
    def __init__(self, est_emprunte: bool):
        self.est_emprunte = est_emprunte

    @abstractmethod
    def emprunter():
        pass

    @abstractmethod
    def rendre():
        pass