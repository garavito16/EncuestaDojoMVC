from encuesta.config.mysqlconnection import connectToMySQL

class Languaje:

    def __init__(self,id,nombre,created_at):
        self.id = id
        self.nombre = nombre
        self.created_at = created_at

    @classmethod
    def getLanguaje(cls):
        query = "SELECT * FROM languaje"
        resultado = connectToMySQL("esquema_encuesta_dojo").query_db(query)
        return resultado