"""
Módulo del Modelo de Acción de Inversión.
Representa una posición financiera individual en un mercado bursátil.
"""

from descriptors import ValidarPrecioAccion


class Accion:
    # Atributo gerenciado mediante el descriptor ValidarPrecioAccion
    precio_actual = ValidarPrecioAccion("precio_actual")

    def __init__(self, ticker: str, cantidad: int, precio_actual: float):
        """
        Inicializa un activo financiero.
        :param ticker: Símbolo bursátil de la empresa (ej. 'AAPL', 'NVDA').
        :param cantidad: Número total de títulos en posesión.
        :param precio_actual: Valor de cotización actual por unidad.
        """
        if cantidad <= 0:
            raise ValueError(
                "La cantidad de títulos poseídos debe ser mayor a cero."
            )

        self.ticker = ticker.strip().upper()
        self.cantidad = int(cantidad)

        # Dispara la ejecución del método __set__ del descriptor `ValidarPrecioAccion`
        self.precio_actual = precio_actual

    @property
    def valor_total(self) -> float:
        """
        Propiedad calculada (@property).
        Retorna el valor de mercado total de la posición (`precio_actual * cantidad`).
        """
        return self.precio_actual * self.cantidad

    def __repr__(self) -> str:
        return f"Accion(ticker='{self.ticker}', cantidad={self.cantidad}, precio_actual=${self.precio_actual:.2f})"


