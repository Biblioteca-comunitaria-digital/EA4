class Usuario:
    """Clase que representa un usuario del sistema."""
    def __init__(self, id_usuario: int, nombre_usuario: str, rol: str):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.rol = rol

    def es_admin(self) -> bool:
        return self.rol == 'admin'

# NUEVA CLASE: Producto
class Producto:
    """Clase que representa un producto del sistema."""
    def __init__(self, id_producto: int, nombre: str, descripcion: str, precio: float, id_usuario: int):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.id_usuario = id_usuario  # ID del usuario creador
    def __str__(self):
        return f"Producto(ID: {self.id_producto}, Nombre: {self.nombre}, Precio: ${self.precio})"

    def __str__(self):
        return f"Usuario(ID: {self.id_usuario}, Nombre: {self.nombre_usuario}, Rol: {self.rol})"

