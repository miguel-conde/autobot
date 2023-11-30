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