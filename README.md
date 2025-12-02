# Análise de Séries Temporais com Covariáveis - Previsão de Volume

Este repositório contém a análise e modelagem de uma série temporal para a previsão de `volume`, como parte do projeto da disciplina de Séries Temporais da FGV EMAp.

## Integrantes

- Gustavo Tironi
- Kauan Mariani Ferreira
- Lívia Verly
- Matheus Fillype Ferreira de Carvalho
- Pedro Henrique Coterli
- Sillas Rocha da Costa

## Objetivo

O projeto visa evoluir de uma análise univariada para uma modelagem multivariada da variável `volume`. O objetivo é incorporar dados de investimento (`inv`) e de usuários ativos (`users`) para verificar se essas informações externas melhoram a precisão das previsões em comparação com modelos de base. O foco é entender o impacto real dessas variáveis de negócio na série temporal de `volume`.

## Metodologia

A abordagem metodológica foi dividida nas seguintes etapas:

1.  **Análise Exploratória Multivariada**:
    *   Visualização das séries (`volume`, `inv`, `users`) para identificar padrões e relações.
    *   Análise de autocorrelação (ACF) e autocorrelação parcial (PACF) da variável `volume` para entender sua estrutura de dependência temporal.
    *   Decomposição STL para investigar componentes de tendência e sazonalidade. Foi identificada heterocedasticidade, levando à aplicação de uma transformação logarítmica na variável `volume`.
    *   Análise de correlação cruzada (CCF) para identificar os lags de impacto das covariáveis `inv` e `users` na variável `volume`.

2.  **Modelagem TSLM (Time Series Linear Model)**:
    *   Ajuste de modelos de regressão linear para capturar a relação estrutural entre as covariáveis e a variável `volume`.
    *   Foram testados três modelos: um simples, um com tendência e um modelo de elasticidade (log-log).
    *   O modelo de **elasticidade com tendência** apresentou o melhor desempenho:
        `log(volume) ~ trend + log(inv_lag1) + log(users_lag1) + log(users_lag8)`

3.  **Diagnóstico de Resíduos**:
    *   Análise dos resíduos do melhor modelo TSLM para verificar as premissas de normalidade, homocedasticidade e independência.
    *   Os resíduos se mostraram normais, mas foi encontrada **autocorrelação significativa**, indicando que a estrutura temporal não foi completamente capturada pelo modelo de regressão.

4.  **ARIMA com Covariáveis (Regressão Dinâmica)**:
    *   Com base na autocorrelação residual do TSLM (principalmente um corte no PACF no lag 1), um modelo ARIMA foi ajustado para modelar essa dinâmica restante.
    *   O modelo final combina a parte estrutural do TSLM com a parte dinâmica do ARIMA para obter previsões mais precisas.

## Validação

A validação do modelo foi realizada simulando um cenário real de previsão, utilizando uma estratégia de *walk-forward* (previsões semana a semana) para horizontes de até 4 semanas à frente, garantindo a robustez dos resultados para uso prático.

## Como Executar

Os notebooks contêm toda a análise e código. Para executá-los, é necessário ter as bibliotecas listadas em `requirements.txt`.

```bash
pip install -r requirements.txt
```

- **`relatorio.ipynb`**: Notebook principal que consolida toda a análise, modelagem e conclusões do projeto.
