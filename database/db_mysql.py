from decouple import config
import pymysql
import pymysql.cursors

class MySQLDatabase:
    def __init__(self):
        self.connection = None

    def connect(self):
        """Conexión con la base de datos."""
        try:
            self.connection = pymysql.connect(
                host=config('MYSQL_HOST'),
                user=config('MYSQL_USER'),
                password=config('MYSQL_PASSWORD'),
                db=config('MYSQL_DB'),
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Conexión exitosa a la base de datos")
        except Exception as ex:
            print(f"Error al conectar a la base de datos: {ex}")
            self.connection = None

    def disconnect(self):
        """Cerrar la conexión con la base de datos."""
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

    def execute_query(self, query: str, params: tuple = None) -> list:
        """Ejecutar una consulta"""
        if not self.connection:
            print("No hay conexión disponible.")
            return []

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Exception as ex:
            print(f"Error al ejecutar la consulta: {ex}")
            return []

    def execute_update(self, query: str, params: tuple = None) -> int:
        """Ejecutar una consulta INSERT, UPDATE o DELETE y devuelve el número de filas afectadas."""
        if not self.connection:
            print("No hay conexión disponible.")
            return 0

        try:
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(query, params)
                self.connection.commit()
                return affected_rows
        except Exception as ex:
            print(f"Error al ejecutar la actualización: {ex}")
            self.connection.rollback()
            return 0
