from flask import flash
from encuesta.config.mysqlconnection import connectToMySQL
from encuesta.models.model_editor import Editor

class Dojo:

    def __init__(self,id,nombre,comentario,sexo,location,languaje,created_at):
        self.id = id
        self.nombre = nombre
        self.comentario = comentario
        self.sexo = sexo
        self.location = location
        self.languaje = languaje
        self.created_at = created_at
        self.editores = []

    def addEditor(self,editor):
        self.editores.append(editor)

    @classmethod
    def getDojo(cls,data):
        query = '''
                    SELECT d.id,d.nombre, d.comentario, (CASE WHEN d.sexo = 'M' THEN 'MASCULINO' WHEN d.sexo = 'F' THEN 'FEMENINO' ELSE 'OTRO' END) AS sexo, 
                    l.nombre AS languaje, d.created_at, lo.nombre AS location, e.id AS editor_id, e.nombre AS editor_nombre, e.created_at AS created_at_editor
                    FROM dojos d 
                    INNER JOIN languaje l ON l.id = d.languaje_id
                    INNER JOIN location lo ON lo.id = d.location_id
                    LEFT JOIN favorites f ON f.dojo_id = d.id
                    LEFT JOIN editor e ON e.id = f.editor_id
                    WHERE d.id = %(id)s;
                '''
        dojo = None
        resultado = connectToMySQL("esquema_encuesta_dojo").query_db(query,data)
        if(len(resultado) > 0):
            dojo = Dojo(resultado[0]["id"],resultado[0]["nombre"],resultado[0]["comentario"],resultado[0]["sexo"],resultado[0]["location"],resultado[0]["languaje"],resultado[0]["created_at"])
            for editor in resultado:
                if(editor["editor_id"] != None):
                    dojo.addEditor(Editor(editor["editor_id"],editor["editor_nombre"],editor["created_at_editor"]))
        return dojo

    @classmethod
    def addDojo(cls,data,favoritos):
        query = "INSERT INTO dojos (nombre,comentario,sexo,location_id,languaje_id,created_at) VALUES (%(nombre)s,%(comentario)s,%(sexo)s,%(location_id)s,%(languaje_id)s,now());"
        dojo_id = connectToMySQL("esquema_encuesta_dojo").query_db3(query,data)
        print(dojo_id)
        if(dojo_id > 0):
            query = "INSERT INTO favorites (dojo_id,editor_id,created_at)VALUES(%(dojo_id)s,%(editor_id)s,now());"
            cont = 0
            aux = 1
            while cont < (len(favoritos)) and aux > 0:
                data = { 
                    "editor_id" : favoritos[cont], 
                    "dojo_id" : dojo_id 
                }
                aux = connectToMySQL("esquema_encuesta_dojo").query_db3(query,data)
                if(aux == 0):
                    return 0
                else:
                    cont += 1
            connectToMySQL("esquema_encuesta_dojo").close_conection()
        return dojo_id

    @classmethod
    def verifyData(cls,dojo):
        is_valid = True
        if(len(dojo["nombre"]) < 3):
            flash("El nombre del ninja debe tener mas de 3 caracteres")
            is_valid = False
        if(len(dojo["sexo"]) == 0):
            flash("Debe seleccionar el sexo del ninja")
            is_valid = False
        if(len(dojo["location_id"]) == 0):
            flash("Debe seleccionar el local del dojo")
            is_valid = False
        if(len(dojo["languaje_id"]) == 0):
            flash("Debe seleccionar el lenguaje favorito del ninja")
            is_valid = False
        return is_valid