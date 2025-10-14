from ..database.database_manager import DatabaseManager
from .models import Producto

class ProductManager:
    """Lógica de negocio para la gestión de productos. Solo accesible por admins."""
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def crear_producto(self, nombre: str, descripcion: str, precio: float, id_usuario: int) -> tuple[bool, str]:
        """Crea un nuevo producto asociado a un usuario (admin)."""
        if not self.db_manager.ejecutar_consulta("SELECT id_usuario FROM usuarios WHERE id_usuario = %s AND id_rol = (SELECT id_rol FROM roles WHERE nombre_rol = 'admin')", (id_usuario,)):
            return False, "Error: Solo admins pueden crear productos."

        query = "INSERT INTO productos (nombre, descripcion, precio, id_usuario) VALUES (%s, %s, %s, %s)"
        params = (nombre, descripcion, precio, id_usuario)

        if self.db_manager.ejecutar_modificacion(query, params):
            return True, "Producto creado exitosamente."
        else:
            return False, "Error al crear el producto."

    def listar_productos(self) -> list[dict]:
        """Devuelve una lista de todos los productos."""
        query = "SELECT * FROM productos ORDER BY id_producto"
        return self.db_manager.ejecutar_consulta(query)

    def listar_productos_con_join(self) -> list[dict]:
        """Listado con JOIN - Muestra productos con nombre del creador (usuario)."""
        query = """
            SELECT p.id_producto, p.nombre, p.descripcion, p.precio, u.nombre_usuario AS creador
            FROM productos p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            ORDER BY p.id_producto
        """
        return self.db_manager.ejecutar_consulta(query)

    def actualizar_producto(self, id_producto: int, nombre: str, descripcion: str, precio: float) -> bool:
        """Actualiza un producto por ID."""
        query = "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s WHERE id_producto = %s"
        params = (nombre, descripcion, precio, id_producto)
        return self.db_manager.ejecutar_modificacion(query, params)

    def eliminar_producto(self, id_producto: int) -> bool:
        """Elimina un producto por ID."""
        query = "DELETE FROM productos WHERE id_producto = %s"
        return self.db_manager.ejecutar_modificacion(query, (id_producto,))
