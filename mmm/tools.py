import numpy as np
import statsmodels.api as sm
from typing import List

from typing import List

def calculate_geom_ad_stock(series: List[float], decay_factor: float, initial_value: float = 0) -> List[float]:
    """
    Calcula el 'ad stock' geométrico de una serie de datos aplicando un factor de decaimiento.

    El 'ad stock' es un concepto en marketing y economía que representa el impacto acumulado
    de la publicidad a lo largo del tiempo. Esta función aplica un modelo de ad stock geométrico,
    donde el efecto de la publicidad se deprecia de forma geométrica en cada período.

    Args:
        series (List[float]): Lista de valores que representan la inversión o impacto publicitario en cada período.
        decay_factor (float): Factor de decaimiento que se aplica a la acumulación de ad stock. 
                              Si es mayor que 1, se considera como porcentaje y se divide por 100.
        initial_value (float, optional): Valor inicial de ad stock. Por defecto es 0.

    Returns:
        List[float]: Lista de valores actualizados representando el ad stock acumulado.

    Example:
    ```
        >>> series = [100, 200, 300, 400]
        >>> decay_factor = 0.9
        >>> initial_value = 50
        >>> calculate_geom_ad_stock(series, decay_factor, initial_value)
        [50.0, 140.0, 266.0, 431.4]
    ```
    """
    updated_series = series.copy()

    # Ajusta el factor de decaimiento si es mayor que 1 (tratándolo como un porcentaje)
    if decay_factor > 1:
        decay_factor = decay_factor / 100

    if len(updated_series) > 1:
        # Actualiza el primer valor de la serie con el valor inicial
        updated_series[0] = updated_series[0] + decay_factor * initial_value

        # Itera a través de la serie, aplicando el factor de decaimiento de forma acumulativa
        for i in range(1, len(updated_series)):
            updated_series[i] = updated_series[i] + decay_factor * updated_series[i-1]

    return updated_series



import numpy as np
import statsmodels.api as sm

def R2(fit: sm.regression.linear_model.RegressionResultsWrapper) -> float:
    """
    Calcula la bondad del ajuste de un modelo estadístico.

    Este método calcula el coeficiente de determinación (R²), que es una medida de qué tan bien
    las variables independientes predicen la variable dependiente. Un R² más alto indica un mejor ajuste
    del modelo.

    Args:
        fit (sm.regression.linear_model.RegressionResultsWrapper): Un modelo ajustado utilizando la biblioteca
                                                                   statsmodels. Este objeto contiene tanto los residuos 
                                                                   como la variable dependiente del modelo.

    Returns:
        float: El coeficiente de determinación R² del modelo.

    Example:
    ```
        >>> import statsmodels.api as sm
        >>> import numpy as np
        >>> x = np.array([1, 2, 3, 4, 5])
        >>> y = np.array([2, 4, 6, 8, 10])
        >>> model = sm.OLS(y, x).fit()
        >>> R2(model)
        1.0
    ```
    """
    # Obteniendo los residuos del modelo
    residuals = fit.resid

    # Calculando la suma de cuadrados de los residuos
    ss_res = np.sum(residuals**2)

    # Calculando la suma total de cuadrados
    ss_tot = np.sum((fit.model.endog - np.mean(fit.model.endog))**2)

    # Calculando R2
    r2 = 1 - (ss_res / ss_tot)

    return r2
