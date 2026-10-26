## 📁 Proyecto 3: Cartera de Inversiones FinTech
Este documento contiene la solución completa, explicada y documentada para el sistema de gestión de portafolios de inversión bursátil, aplicando patrones avanzados de Programación Orientada a Objetos en Python y respetando las buenas prácticas de arquitectura limpia.

## 📌 ¿Por qué este proyecto? (Conceptos Clave de POO)
En el sector financiero y FinTech, la precisión numérica, la validación estricta de límites y la inmutabilidad de los datos son requisitos fundamentales de arquitectura de software. En este proyecto aplicamos:

-Descriptores Financieros Reusables (ValidarPrecioAccion):

-El Problema: Múltiples activos o transacciones requieren asegurar que las cotizaciones bursátiles o precios de mercado sean estrictamente mayores a $0.0, además de poder parsear datos que provienen de APIs externas en formato texto.

La Solución: Implementar un Descriptor con los métodos mágicos __get__ y __set__ que intercepta las asignaciones de variables numéricas, valida el tipo, convierte cadenas numéricas limpias y rechaza importes nulos o negativos antes de escribirlos en instance.__dict__.

-Propiedades Calculadas (@property):

-Evaluación en tiempo real del valor de mercado individual de una posición (valor_total = precio_actual * cantidad) y del portafolio consolidado (balance_total), evitando estados inconsistentes o duplicación de atributos en memoria.

-Métodos Estáticos de Utilidad (@staticmethod):

-La función es_ticker_valido(ticker) utiliza Expresiones Regulares (re) para validar la nomenclatura internacional de símbolos bursátiles (de 1 a 5 letras mayúsculas, ej: "AAPL", "NVDA"). Es una utilidad pura sin acceso a self ni cls.

-Sobrecarga de Métodos Dunder y Operadores (__add__, __len__, __getitem__):

-Operador + (__add__): Permite incorporar una Accion directamente al Portafolio mediante la sintaxis natural portafolio + accion.

-Colecciones (__len__ y __getitem__): Transforma la cartera en una colección indexable y consultable mediante len(portafolio) y bucles for.
```text
📁 Arquitectura del Proyecto
Plaintext
CarteraInversiones Fintech/
│
├── descriptors.py        # Descriptor ValidarPrecioAccion (Protocolo __get__/__set__)
├── AccionInversion.py    # Modelo de Activo Bursátil (Accion)
├── Portafolio.py         # Cartera de inversión y gestor de posiciones
├── main.py               # Script de ejecucion y suite de pruebas financieras
└── README.md             # Documentación técnica explicativa del proyecto
```
💻 Código Fuente Completo
### 📄 File: `descriptors.py`

```python
"""
Módulo de Descriptores Financieros.
Provee validación reusable de precios e importes para instrumentos de inversión.
"""


class ValidarPrecioAccion:

    def __init__(self, nombre_atributo: str):
        """
        Constructor del descriptor.
        :param nombre_atributo: Nombre de la clave privada que se guardará en `instance.__dict__`.
        """
        self.nombre_atributo = nombre_atributo

    def __get__(self, instance, owner):
        """Invocado automáticamente al LEER el atributo (ej: accion.precio_actual)."""
        if instance is None:
            return self
        return instance.__dict__.get(self.nombre_atributo)

    def __set__(self, instance, value):
        """
        Invocado automáticamente al ASIGNAR un valor (ej: accion.precio_actual = 150.0).
        Garantiza que el precio sea mayor a cero y convierte cadenas de texto numéricas a float.
        """
        # Permite sanitizar cadenas numéricas provenientes de APIs o inputs del usuario
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                raise TypeError(
                    "El precio de la acción debe ser un número entero o flotante válido."
                )

        # Validación estricta de tipo de dato
        if not isinstance(value, (int, float)):
            raise TypeError("El precio debe ser de tipo entero o float.")

        # Validación financiera: Precio estrictamente mayor a 0.0
        if value <= 0.0:
            raise ValueError(
                "El precio actual de una acción debe ser estrictamente mayor que $0.0."
            )

        instance.__dict__[self.nombre_atributo] = float(value)
```

---

### 📄 File: `AccionInversion.py`

```python
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
        Propiedad calculada (@property) de solo lectura.
        Retorna el valor de mercado total de la posición (`precio_actual * cantidad`).
        """
        return self.precio_actual * self.cantidad

    def __repr__(self) -> str:
        """Representación oficial del objeto para depuración."""
        return f"Accion(ticker='{self.ticker}', cantidad={self.cantidad}, precio_actual=${self.precio_actual:.2f})"
```

---

### 📄 File: `Portafolio.py`

```python
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
```

---

### 📄 File: `main.py`

```python
"""
Punto de Entrada Principal (Main Script) - Cartera de Inversiones FinTech.
Ejecuta las validaciones de mercado, adición de activos mediante sobrecarga de operadores
y evaluación del balance total de la cartera.
"""

from AccionInversion import Accion
from Portafolio import Portafolio

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PRUEBA EJERCICIO 3: PORTAFOLIO Y ACCIONES (FINTECH)")
    print("=" * 60)

    # 1. Creación de Activos Financieros
    a1 = Accion(ticker="AAPL", cantidad=10, precio_actual=150.0)
    a2 = Accion(ticker="NVDA", cantidad=5, precio_actual=400.0)

    print(f"Activo 1: {a1} | Valor Total: ${a1.valor_total:.2f}")
    print(f"Activo 2: {a2} | Valor Total: ${a2.valor_total:.2f}")

    # 2. Inicialización del Portafolio y Suma con Operador '+'
    portafolio = Portafolio("Bruno Lezama")
    portafolio = portafolio + a1  # Dispara Portafolio.__add__
    portafolio = portafolio + a2

    # 3. Pruebas de Propiedades y Métodos Estáticos
    print(
        f"\nTicker 'AAPL' es válido: {Portafolio.es_ticker_valido('AAPL')}"
    )
    print(
        f"Ticker 'GOOGLE123' es válido: {Portafolio.es_ticker_valido('GOOGLE123')}"
    )

    print(f"\nAcciones distintas en cartera (__len__): {len(portafolio)}")
    print(f"Balance Total del Portafolio: ${portafolio.balance_total:.2f}")

    # 4. Prueba de error en descriptor financiero
    print("\n" + "-" * 40)
    print("PRUEBA DE VALIDACIÓN EN DESCRIPTOR FINANCIERO")
    print("-" * 40)

    try:
        a_error = Accion(ticker="TSLA", cantidad=2, precio_actual=-50.0)
    except ValueError as err:
        print(f"[ÉXITO] Captura de precio negativo en la acción: {err}")
```
# 🧪 Salida Esperada al Ejecutar
```python

Plaintext
============================================================
PRUEBA EJERCICIO 3: PORTAFOLIO Y ACCIONES (FINTECH)
============================================================
Activo 1: Accion(ticker='AAPL', cantidad=10, precio_actual=$150.00) | Valor Total: $1500.00
Activo 2: Accion(ticker='NVDA', cantidad=5, precio_actual=$400.00) | Valor Total: $2000.00

Ticker 'AAPL' es válido: True
Ticker 'GOOGLE123' es válido: False

Acciones distintas en cartera (__len__): 2
Balance Total del Portafolio: $3500.00

----------------------------------------
PRUEBA DE VALIDACIÓN EN DESCRIPTOR FINANCIERO
----------------------------------------
[ÉXITO] Captura de precio negativo en la acción: El precio actual de una acción debe ser estrictamente mayor que $0.0.
