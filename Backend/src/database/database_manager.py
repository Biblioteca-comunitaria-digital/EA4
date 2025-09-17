import mysql.connector
from mysql.connector import errorcode

class DatabaseManager:
    """
    Gestiona la conexión y las operaciones con la base de datos MySQL.
    """
    def __init__(self, db_config: dict):
        """
        Inicializa el gestor con la configuración de la base de datos.
        :param db_config: Diccionario con 'host', 'user', 'password', 'database'.
        """
        self.db_config = db_config
        self.conn = None
        self.cursor = None

    def conectar(self):
        """Establece la conexión con la base de datos."""
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            print("Conexión a MySQL establecida exitosamente.")
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Usuario o contraseña de la base de datos incorrectos.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: La base de datos no existe.")
            else:
                print(f"Error al conectar con la base de datos: {err}")
            self.conn = None
            return False

    def desconectar(self):
        """Cierra el cursor y la conexión con la base de datos."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Conexión a MySQL cerrada.")

    def ejecutar_consulta(self, query: str, params: tuple = ()) -> list[dict]:
        """
        Ejecuta una consulta SELECT y devuelve los resultados como una lista de diccionarios.
        """
        if not self.conn or not self.conn.is_connected():
            print("Error: No hay conexión a la base de datos.")
            return []
        try:
            # Usar un cursor de diccionario para obtener resultados como {columna: valor}
            self.cursor = self.conn.cursor(dictionary=True)
            self.cursor.execute(query, params)
            resultados = self.cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print(f"Error al ejecutar consulta: {err}")
            return []

    def ejecutar_modificacion(self, query: str, params: tuple = ()) -> bool:
        """
        Ejecuta una consulta de modificación (INSERT, UPDATE, DELETE).
        Devuelve True si la operación fue exitosa, False en caso contrario.
        """
        if not self.conn or not self.conn.is_connected():
            print("Error: No hay conexión a la base de datos.")
            return False
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(query, params)
            self.conn.commit() # Confirmar la transacción
            return True
        except mysql.connector.Error as err:
            print(f"Error al ejecutar modificación: {err}")
            self.conn.rollback() # Revertir cambios en caso de error
            return False

    def ejecutar_script(self, script_path: str):
        """Ejecuta un script SQL desde un archivo."""
        if not self.conn or not self.conn.is_connected():
            print("Error: No hay conexión a la base de datos.")
            return

        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                # Separar los comandos del script por punto y coma
                sql_commands = f.read().split(';')

            self.cursor = self.conn.cursor()
            for command in sql_commands:
                # Ejecutar solo si el comando no está vacío o es solo un espacio en blanco
                if command.strip():
                    self.cursor.execute(command)
            self.conn.commit()
            print(f"Script '{script_path}' ejecutado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al ejecutar script: {err}")
            self.conn.rollback()