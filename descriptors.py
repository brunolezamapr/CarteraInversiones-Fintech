
class ValidarPrecioAccion:

    def __init__(self, nombre_atributo: str):
        self.nombre_atributo = nombre_atributo

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.nombre_atributo)

    def __set__(self, instance, value):
        # Permite convertir cadenas numéricas limpias si provienen de inputs/API
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                raise TypeError(
                    "El precio debe ser de tipo entero o float."
                )

        if not isinstance(value, (int, float)):
            raise TypeError("Precio debe ser de tipo entero o float")

        if value <= 0.0:
            raise ValueError(
                "El precio de la acción debe ser estrictamente mayor a 0"
            )

        instance.__dict__[self.nombre_atributo] = float(value)