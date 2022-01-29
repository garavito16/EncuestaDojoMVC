# un cursor es el objeto que usamos para interactuar con la base de datos
import pymysql.cursors
# esta clase nos dará una instancia de una conexión a nuestra base de datos
class MySQLConnection:

    def __init__(self, db):
        # cambiar el usuario y la contraseña según sea necesario
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root',
                                    password = 'root',
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = False)
        # establecer la conexión a la base de datos
        self.connection = connection
        self.conexion = None
    

    # el método para consultar la base de datos
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # las consultas INSERT devolverán el NÚMERO DE ID de la fila insertada
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # las consultas SELECT devolverán los datos de la base de datos como una LISTA DE DICCIONARIOS
                    result = cursor.fetchall()
                    return result
                else:
                    # las consultas UPDATE y DELETE no devolverán nada
                    self.connection.commit()
            except Exception as e:
                # si la consulta falla, el método devolverá FALSE
                print("Something went wrong", e)
                return False
            finally:
                # cerrar la conexión
                self.connection.close()
    
    
    def execute_query(self,query,data):
        # if (self.connection.cursor() != None):
            with self.devolver_cursor() as cursor:
                try:
                    query = cursor.mogrify(query, data)
                    print("Running Query:", query)
                    cursor.execute(query, data)
                    # self.connection.commit()
                    return cursor.lastrowid
                except Exception as e:
                    # si la consulta falla, el método devolverá FALSE
                    print("Something went wrong", e)
                    self.connection.rollback()
                    self.connection.commit()
                    self.connection.close()
                    return False
    
    def close_conection(self):
        self.connection.commit()
        self.connection.close()

    def devolver_cursor(self):
        if (self.conexion == None):
            self.connection.begin()
            self.conexion = self.connection.cursor()
        return self.conexion
        


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

    
# connectToMySQL recibe la base de datos que estamos usando y la usa para crear una instancia de MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
