# un cursor es el objeto que usamos para interactuar con la base de datos
import pymysql.cursors
# esta clase nos dará una instancia de una conexión a nuestra base de datos
class MySQLConnection:

    conexion = None

    def __init__(self, db):
        if(self.devolver_conexion() == None):
            print("inicio la conexion")
            # cambiar el usuario y la contraseña según sea necesario
            connection = pymysql.connect(host = 'localhost',
                                        user = 'root',
                                        password = 'root',
                                        db = db,
                                        charset = 'utf8mb4',
                                        cursorclass = pymysql.cursors.DictCursor,
                                        autocommit = False)
            # establecer la conexión a la base de datos
            MySQLConnection.conexion = connection
        self.conexion = MySQLConnection.conexion
    
    @classmethod
    def devolver_conexion(self):
        print(MySQLConnection.conexion)
        if(MySQLConnection.conexion != None):
            return MySQLConnection.conexion
        else:
            return None

    def query_db3(self, query, data):
        
        with self.conexion.cursor() as cursor:
            try:
                # self.conexion.begin()
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query, data)
                return cursor.lastrowid
                # self.conexion.commit()
                    
            except Exception as e:
                # si la consulta falla, el método devolverá FALSE
                print("Something went wrong", e)
                self.conexion.rollback()
                self.conexion.close()
                MySQLConnection.conexion = None
                return 0
    
    def close_conection(self):
        self.conexion.commit()
        self.conexion.close()
        MySQLConnection.conexion = None

    # el método para consultar la base de datos
    def query_db(self, query, data=None):
        with self.conexion.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # las consultas INSERT devolverán el NÚMERO DE ID de la fila insertada
                    self.conexion.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # las consultas SELECT devolverán los datos de la base de datos como una LISTA DE DICCIONARIOS
                    result = cursor.fetchall()
                    return result
                else:
                    # las consultas UPDATE y DELETE no devolverán nada
                    self.conexion.commit()
            except Exception as e:
                # si la consulta falla, el método devolverá FALSE
                print("Something went wrong", e)
                return False
            finally:
                # cerrar la conexión
                self.conexion.close()
                MySQLConnection.conexion = None


    ''' funciona este codigo
    def query_db3(self, query, data, query2, data2):
        print("revisando la conexion 2")
        print(self.connection.open)
        with self.connection.cursor() as cursor:
            print("revisando la conexion 3")
            print(self.connection.open)
            try:
                self.connection.begin()
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                cursor.execute(query, data)
                aux = cursor.lastrowid

                for index in range (len(data2)):
                    data2[index]["dojo_id"] = aux
                    cursor.execute(query2, data2[index])
                
                self.connection.commit()
                    
            except Exception as e:
                # si la consulta falla, el método devolverá FALSE
                print("Something went wrong", e)
                self.connection.rollback()
                return False
            finally:
                # cerrar la conexión
                self.connection.close()
    '''

    
# connectToMySQL recibe la base de datos que estamos usando y la usa para crear una instancia de MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
