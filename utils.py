from abc import ABC, abstractmethod
class ForecastingStrategy(ABC):
    """Interface do modelo"""
    
    @abstractmethod
    def fit(self, y_train, X_train=None):
        """Treina o modelo com os dados passados."""
        pass

    @abstractmethod
    def predict(self, steps, X_future=None):
        """Retorna a previsão (array) e as datas (index)."""
        pass
    
    @property
    @abstractmethod
    def name(self): pass
    

class MetricStrategy(ABC):
    @abstractmethod
    def calculate(self, y_true, y_pred):
        pass
    
    @property
    @abstractmethod
    def name(self):
        pass