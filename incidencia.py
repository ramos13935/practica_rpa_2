class Incidencia:
    def __init__(self, nombre, apellido, email, telefono, codigo_incidencia, nombre_incidencia, estado_incidencia):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = str(telefono)
        self.codigo_incidencia = codigo_incidencia
        self.nombre_incidencia = nombre_incidencia
        self.estado_incidencia = estado_incidencia

    def __str__(self):
        # return f"{self.codigo_operacion}; {self.nombre_operacion}; {self.estado_operacion}"
        return f"Incidencia Num. {self.codigo_incidencia} - {self.nombre_incidencia} - {str(self.estado_incidencia).upper()}"
