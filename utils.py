from abc import ABC, abstractmethod
import numpy as np
from scipy.stats import norm

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
    
# Métricas utilizadas
def winkler_score(y_true, lower, upper, alpha):
    score = np.where(
        y_true < lower,
        (upper - lower) + (2 / alpha) * (lower - y_true),
        np.where(y_true > upper, (upper - lower) + (2 / alpha) * (y_true - upper), (upper - lower))
    )
    return np.mean(score)

def quantile_score(y_true, quantile_forecast, p):
    error = y_true - quantile_forecast
    return np.mean(np.where(error >= 0, p * error, (p - 1) * error))

def crps_gaussian(y_true, mu, sigma):
    sigma = np.where(sigma < 1e-6, 1e-6, sigma)
    z = (y_true - mu) / sigma
    crps = sigma * (z * (2 * norm.cdf(z) - 1) + 2 * norm.pdf(z) - 1 / np.sqrt(np.pi))
    return np.mean(crps)

class RMSE(MetricStrategy):
    def calculate(self, group): 
        return np.sqrt(np.mean((group['prediction'] - group['actual'])**2))
    @property
    def name(self): 
        return "RMSE"

class MAE(MetricStrategy):
    def calculate(self, group): 
        return np.mean(np.abs(group['prediction'] - group['actual']))
    @property
    def name(self): 
        return "MAE"

class WinklerScore(MetricStrategy):
    def __init__(self, alpha=0.05): 
        self.alpha = alpha
    def calculate(self, group): 
        return winkler_score(group['actual'], group['lower_bound'], group['upper_bound'], self.alpha)
    @property
    def name(self): 
        return f"Winkler Score (a={self.alpha})"

class CRPS(MetricStrategy):
    def calculate(self, group): 
        return crps_gaussian(group['actual'], group['prediction'], group['sigma'])
    @property
    def name(self): 
        return "CRPS"

class AvgQuantileScore(MetricStrategy):
    def __init__(self, quantiles=(0.1, 0.25, 0.5, 0.75, 0.9)): 
        self.quantiles = quantiles
    def calculate(self, group):
        scores = []
        for p in self.quantiles:
            q_forecast = norm.ppf(p, loc=group['prediction'], scale=group['sigma'])
            scores.append(quantile_score(group['actual'], q_forecast, p))
        return np.mean(scores)
    @property
    def name(self): 
        return "Avg Quantile Score"