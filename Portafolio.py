"""
Módulo del Modelo de Portafolio Financiero.
Administra un conjunto de acciones, proveyendo utilidades estáticas de validación de Tickers,
balance dinámico y sobrecarga del operador '+' para incorporar activos a la cartera.
"""

import re
from typing import List
from AccionInversion import Accion


class Portafolio:

    def __init__(self, inversionista: str):
        """Inicializa una cartera de inversión vacía."""
        self.inversionista = inversionista
        self._acciones: List[Accion] = []

    @staticmethod
    def es_ticker_valido(ticker: str) -> bool:
        """
        Método Estático (@staticmethod):
        Valida que el símbolo bursátil (ticker) consista de 1 a 5 letras mayúsculas (ej: 'TSLA', 'AAPL').
        """
        if not isinstance(ticker, str):
            return False
        return bool(re.match(r"^[A-Z]{1,5}$", ticker.strip()))

    @property
    def balance_total(self) -> float:
        """
        Propiedad calculada (@property).
        Suma los valores totales de mercado de cada una de las posiciones abiertas en el portafolio.
        """
        return sum(accion.valor_total for accion in self._acciones)

    # --- SOBRECARGA DE MÉTODOS DUNDER ---

    def __len__(self) -> int:
        """Devuelve la cantidad total de posiciones de acciones distintas registradas."""
        return len(self._acciones)

    def __getitem__(self, index: int) -> Accion:
        """Permite acceder a una acción por su posición o iterar sobre el portafolio."""
        return self._acciones[index]

    def __add__(self, otra_accion: Accion) -> "Portafolio":
        """
        Sobrecarga del Operador de Suma (`+`):
        Permite añadir una `Accion` directamente a la cartera (`portafolio + accion`).
        """
        if isinstance(otra_accion, Accion):
            self._acciones.append(otra_accion)
            return self
        return NotImplemented

    def __repr__(self) -> str:
        return f"Portafolio(inversionista='{self.inversionista}', balance_total=${self.balance_total:.2f})"