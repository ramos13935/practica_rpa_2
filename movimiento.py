class Movimiento:
    def __init__(self, nombre, apellido, email, codigo_operacion, nombre_operacion, estado_operacion):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.codigo_operacion = codigo_operacion
        self.nombre_operacion = nombre_operacion
        self.estado_operacion = estado_operacion

    def __str__(self):
        return f"{self.codigo_operacion}; {self.nombre_operacion}; {self.estado_operacion}"
