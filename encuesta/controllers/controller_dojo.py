

from flask import Flask, redirect, render_template, request, session, flash
from encuesta import app
from encuesta.models.model_location import Location
from encuesta.models.model_languaje import Languaje
from encuesta.models.model_editor import Editor
from encuesta.models.model_dojo import Dojo

@app.route('/')
def initial():
    languajes = Languaje.getLanguaje()
    locations = Location.getLocation()
    editors = Editor.getEditor()
    return render_template('index.html',locations=locations,languajes=languajes,editors=editors)

@app.route('/process',methods=["POST"])
def process():
    dojo = {
        "nombre" : request.form["input_name"],
        "location_id" : request.form["select_location"],
        "languaje_id" : request.form["select_languaje"],
        "comentario" : request.form["input_comment"],
        "sexo" : request.form["input_sexo"]
    }
    if Dojo.verifyData(dojo):
        favoritos = []
        for i in request.form.getlist("input_check"):
            favoritos.append(i)
        resultado = Dojo.addDojo(dojo,favoritos)

        if(resultado > 0):
            return redirect('/result/'+str(resultado))
        else:
            flash("No se pudo realizar el registro")
            return redirect('/')
    else:
        return redirect('/')

@app.route('/result/<id_dojo>')
def result(id_dojo):
    dojo = {
        "id" : id_dojo
    }
    dojo = Dojo.getDojo(dojo)
    if(dojo == None):
        flash("Hubo un error al cargar los datos")
        return redirect('/')
    else:
        return render_template('result.html',dojo=dojo)
