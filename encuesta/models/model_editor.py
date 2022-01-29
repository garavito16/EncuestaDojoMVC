from encuesta.config.mysqlconnection import connectToMySQL

class Editor:

    def __init__(self,id,nombre,created_at):
        self.id = id
        self.nombre = nombre
        self.created_at = created_at

    @classmethod
    def getEditor(cls):
        query = "SELECT * FROM editor"
        resultado = connectToMySQL("esquema_encuesta_dojo").query_db(query)
        return resultado