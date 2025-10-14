import stdiomask  
from .database.database_manager import DatabaseManager
from .modulo1.services import UserManager
from .modulo1.models import Usuario
from .modulo1.product_manager import ProductManager  
from .utils import limpiar_consola, validar_contraseña

# --- CONFIGURACIÓN DE LA BASE DE DATOS MYSQL ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'app_idp',
    'password': 'admin123',
    'database': 'gestion_usuarios_db',
    'port': 3307
}

SCRIPT_PATH = 'src/database/create_database.sql'

class Application:
    def __init__(self):
        self.db_manager = DatabaseManager(DB_CONFIG)
        self.user_manager = UserManager(self.db_manager)
        self.product_manager = ProductManager(self.db_manager) 
        self.usuario_actual: Usuario | None = None

    def inicializar_bd(self):
        """Crea la BD y las tablas si no existen."""
        print("Intentando conectar a la base de datos...")
        if not self.db_manager.conectar():
            print("Fallo crítico: No se pudo conectar a la base de datos. El programa se cerrará.")
            exit()

        tablas = self.db_manager.ejecutar_consulta("SHOW TABLES LIKE 'usuarios';")
        if not tablas:
            print("Tablas no encontradas. Ejecutando script de creación...")
            self.db_manager.ejecutar_script(SCRIPT_PATH)
        else:
            print("Las tablas de la base de datos ya existen.")
        self.db_manager.desconectar()

    def mostrar_menu_principal(self):
        limpiar_consola()
        print("===== BIENVENIDO AL SISTEMA DE GESTIÓN DE USUARIOS Y PRODUCTOS =====")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        return input("Seleccione una opción: ")

    def accion_registrar(self):
        limpiar_consola()
        print("--- Registro de Nuevo Usuario ---")
        nombre_usuario = input("Nombre de usuario: ")
        email = input("Email: ")
        
        while True:
            print("Contraseña: ", end='', flush=True)
            contraseña = stdiomask.getpass(prompt='', mask='*')
            
            es_valida, mensaje = validar_contraseña(contraseña)
            if es_valida:
                print("Confirme la contraseña: ", end='', flush=True)
                contraseña_confirm = stdiomask.getpass(prompt='', mask='*')

                if contraseña == contraseña_confirm:
                    break
                else:
                    print("Las contraseñas no coinciden. Intente de nuevo.")
            else:
                print(f"Error: {mensaje}")

        exito, mensaje = self.user_manager.registrar_usuario(nombre_usuario, email, contraseña)
        print(mensaje)
        input("\nPresione Enter para continuar...")

    def accion_iniciar_sesion(self):
        limpiar_consola()
        print("--- Inicio de Sesión ---")
        nombre_usuario = input("Nombre de usuario: ")

        print("Contraseña: ", end='', flush=True)
        contraseña = stdiomask.getpass(prompt='', mask='*')
        
        usuario, mensaje = self.user_manager.iniciar_sesion(nombre_usuario, contraseña)
        print(mensaje)
        
        if usuario:
            self.usuario_actual = usuario
            self.mostrar_menu_sesion_iniciada()
        else:
            input("\nPresione Enter para continuar...")

    def mostrar_menu_sesion_iniciada(self):
        if self.usuario_actual.es_admin():
            self.menu_admin()
        else:
            self.menu_estandar()
        self.usuario_actual = None 

    def menu_estandar(self):
        while True:
            limpiar_consola()
            print(f"--- MENÚ DE USUARIO ESTÁNDAR - Bienvenido, {self.usuario_actual.nombre_usuario} ---")
            print("1. Ver mis datos")
            print("2. Cerrar Sesión")
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                print("\n--- Tus Datos ---")
                print(f"ID de Usuario: {self.usuario_actual.id_usuario}")
                print(f"Nombre de Usuario: {self.usuario_actual.nombre_usuario}")
                print(f"Rol: {self.usuario_actual.rol}")
                input("\nPresione Enter para volver...")
            elif opcion == '2':
                print("Cerrando sesión...")
                break
            else:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")

    def menu_admin(self):
        while True:
            limpiar_consola()
            print(f"--- MENÚ DE ADMINISTRADOR - Bienvenido, {self.usuario_actual.nombre_usuario} ---")
            print("1. Ver listado de usuarios")
            print("2. Cambiar rol de un usuario")
            print("3. Eliminar un usuario")
            print("4. Crear Producto")  # NUEVO
            print("5. Listar Productos")  # NUEVO
            print("6. Listar Productos con Creador (JOIN)")  # NUEVO
            print("7. Actualizar Producto")  # NUEVO
            print("8. Eliminar Producto")  # NUEVO
            print("9. Cerrar Sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.accion_admin_ver_usuarios()
            elif opcion == '2':
                self.accion_admin_cambiar_rol()
            elif opcion == '3':
                self.accion_admin_eliminar_usuario()
            elif opcion == '4':  # NUEVO
                self.accion_admin_crear_producto()
            elif opcion == '5':  # NUEVO
                self.accion_admin_listar_productos()
            elif opcion == '6':  # NUEVO
                self.accion_admin_listar_productos_join()
            elif opcion == '7':  # NUEVO
                self.accion_admin_actualizar_producto()
            elif opcion == '8':  # NUEVO
                self.accion_admin_eliminar_producto()
            elif opcion == '9':
                print("Cerrando sesión...")
                break
            else:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")

    def accion_admin_ver_usuarios(self):
        usuarios = self.user_manager.obtener_todos_los_usuarios()
        print("\n--- Listado de Usuarios Registrados ---")
        print("{:<5} {:<20} {:<25} {:<10}".format("ID", "Usuario", "Email", "Rol"))
        print("-" * 65)
        for user in usuarios:
            print("{:<5} {:<20} {:<25} {:<10}".format(user['id_usuario'], user['nombre_usuario'], user['email'], user['nombre_rol']))
        input("\nPresione Enter para volver...")

    def accion_admin_cambiar_rol(self):
        try:
            id_usuario = int(input("Ingrese el ID del usuario a modificar: "))
            nuevo_rol = input("Ingrese el nuevo rol (admin/estandar): ").lower()
            if nuevo_rol not in ['admin', 'estandar']:
                print("Rol no válido.")
            elif self.user_manager.cambiar_rol_usuario(id_usuario, nuevo_rol):
                print("Rol actualizado exitosamente.")
            else:
                print("No se pudo actualizar el rol. Verifique el ID del usuario.")
        except ValueError:
            print("ID no válido. Debe ser un número.")
        input("\nPresione Enter para volver...")

    def accion_admin_eliminar_usuario(self):
        try:
            id_usuario = int(input("Ingrese el ID del usuario a eliminar: "))
            if id_usuario == self.usuario_actual.id_usuario:
                print("No puedes eliminarte a ti mismo.")
            else:
                confirmacion = input(f"¿Está seguro que desea eliminar al usuario con ID {id_usuario}? (s/n): ").lower()
                if confirmacion == 's':
                    if self.user_manager.eliminar_usuario(id_usuario):
                        print("Usuario eliminado exitosamente.")
                    else:
                        print("No se pudo eliminar el usuario.")
        except ValueError:
            print("ID no válido. Debe ser un número.")
        input("\nPresione Enter para volver...")
    
#  CRUD PRODUCTOS
    def accion_admin_crear_producto(self):
        limpiar_consola()
        print("--- Crear Nuevo Producto ---")
        nombre = input("Nombre del producto: ")
        descripcion = input("Descripción: ")
        try:
            precio = float(input("Precio: "))
            if precio <= 0:
                print("El precio debe ser mayor a 0.")
                input("\nPresione Enter para volver...")
                return
        except ValueError:
            print("Precio inválido. Debe ser un número.")
            input("\nPresione Enter para volver...")
            return

        exito, mensaje = self.product_manager.crear_producto(nombre, descripcion, precio, self.usuario_actual.id_usuario)
        print(mensaje)
        input("\nPresione Enter para volver...")

    def accion_admin_listar_productos(self):
        productos = self.product_manager.listar_productos()
        print("\n--- Listado de Productos ---")
        print("{:<5} {:<30} {:<50} {:<10}".format("ID", "Nombre", "Descripción", "Precio"))
        print("-" * 100)
        for prod in productos:
            print("{:<5} {:<30} {:<50} {:<10}".format(prod['id_producto'], prod['nombre'], prod['descripcion'][:47] + "...", f"${prod['precio']}"))
        input("\nPresione Enter para volver...")

    def accion_admin_listar_productos_join(self):
        """NUEVO: Listado con JOIN - Cumple requerimiento de consulta con JOIN."""
        productos = self.product_manager.listar_productos_con_join()
        print("\n--- Listado de Productos con Creador (JOIN) ---")
        print("{:<5} {:<30} {:<50} {:<10} {:<20}".format("ID", "Nombre", "Descripción", "Precio", "Creador"))
        print("-" * 120)
        for prod in productos:
            print("{:<5} {:<30} {:<50} {:<10} {:<20}".format(
                prod['id_producto'], 
                prod['nombre'], 
                prod['descripcion'][:47] + "...", 
                f"${prod['precio']}", 
                prod['creador']
            ))
        input("\nPressione Enter para volver...")

    def accion_admin_actualizar_producto(self):
        try:
            id_producto = int(input("Ingrese el ID del producto a actualizar: "))
            nombre = input("Nuevo nombre: ")
            descripcion = input("Nueva descripción: ")
            precio = float(input("Nuevo precio: "))
            if self.product_manager.actualizar_producto(id_producto, nombre, descripcion, precio):
                print("Producto actualizado exitosamente.")
            else:
                print("No se pudo actualizar el producto. Verifique el ID.")
        except ValueError:
            print("ID o precio inválido. Debe ser un número.")
        input("\nPresione Enter para volver...")

    def accion_admin_eliminar_producto(self):
        try:
            id_producto = int(input("Ingrese el ID del producto a eliminar: "))
            confirmacion = input(f"¿Está seguro que desea eliminar el producto con ID {id_producto}? (s/n): ").lower()
            if confirmacion == 's':
                if self.product_manager.eliminar_producto(id_producto):
                    print("Producto eliminado exitosamente.")
                else:
                    print("No se pudo eliminar el producto.")
        except ValueError:
            print("ID no válido. Debe ser un número.")
        input("\nPresione Enter para volver...")

    def run(self):
        self.inicializar_bd()
        while True:
            opcion = self.mostrar_menu_principal()

            if self.db_manager.conectar():
                if opcion == '1':
                    self.accion_iniciar_sesion()
                elif opcion == '2':
                    self.accion_registrar()
                elif opcion == '3':
                    print("¡Hasta luego!")
                    self.db_manager.desconectar()
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")
                    input("\nPresione Enter para continuar...")

                self.db_manager.desconectar()
            else:
                print("No se pudo conectar a la base de datos para realizar la operación.")
                input("\nPresione Enter para reintentar la conexión o salir...")

if __name__ == '__main__':
    app = Application()
    app.run()
