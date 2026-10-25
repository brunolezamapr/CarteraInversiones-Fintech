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
        """Invocado al acceder a `accion.precio_actual`."""
        if instance is None:
            return self
        return instance.__dict__.get(self.nombre_atributo)

    def __set__(self, instance, value):
        """
        Invocado al asignar `accion.precio_actual = monto`.
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