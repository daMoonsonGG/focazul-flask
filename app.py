from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from patrocinadores import patrocinadores
from users import users
from logged_users import logged_users

@app.route("/")
@cross_origin()
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route("/ping")
def ping():
    return jsonify({"message": "Pong"})

@app.route("/users")
def getUsers():
    return jsonify({"users": users, "message": "Lista de usuarios"})

@app.route("/users/<int:user__id>")
def getUser(user__id):
    usersFound = [user for user in users if user["_id"] == user__id]
    if (len(usersFound) > 0):
        return jsonify({"user": usersFound[0]})  
    return jsonify({"message": "Usuario no existente"})

@app.route("/users/logged-users", methods=["POST"])
def loginUser():
    new_loggedUser = {
        "_id": len(logged_users),
        "name": request.json["name"],
        "email": request.json["email"],
        "status": "logged"
    }
    logged_users.append(new_loggedUser)
    return jsonify({"message": "Usuario conectado", "Usuarios": logged_users})

@app.route("/users/logged-users/<int:logged_user__id>")
def checkUserStatus(logged_user__id):
    logged_usersFound = [logged_user for logged_user in logged_users if logged_user["_id"] == logged_user__id]
    if (len (logged_usersFound) > 0):
        return jsonify({
            "message": "Usuario conectado", "user": logged_usersFound[0]
        })
    return jsonify({
        "message": "Usuario no conectado"
    })

@app.route("/users/logged-users/<int:logged_user__id>", methods=["DELETE"])
def logoutUser(logged_user__id):
    usersFound = [logged_user for logged_user in logged_users if logged_user["_id"] == logged_user__id]
    if (len(usersFound) > 0):
        logged_users.remove(usersFound[0])
        return jsonify({
            "message": "Usuario desconectado"
        }) 
    return jsonify({
        "message": "Usuario no encontrado"
    })

@app.route("/patrocinadores")
def getPatrocinadores():
    response = jsonify({"patrocinadores": patrocinadores, "message": "Lista de patrocinadores"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/patrocinadores/<int:patrocinador__id>")
def getPatrocinador(patrocinador__id):
    patrocinadoresFound = [patrocinador for patrocinador in patrocinadores if patrocinador["_id"] == patrocinador__id]
    if (len(patrocinadoresFound) > 0):
        return jsonify({"patrocinador": patrocinadoresFound[0]})  
    return jsonify({"message": "Patrocinador non existente"})

@app.route("/patrocinadores", methods=["POST"])
def addPatrocinador():
    new_patrocinador = {
        "_id": len(patrocinadores),
        "name": request.json["name"],
        "href": request.json["href"],
        "img_src": request.json["img_src"],
    }
    patrocinadores.append(new_patrocinador)
    return jsonify({"message": "Patrocinador agregado", "patrocinadores": patrocinadores})

@app.route("/patrocinadores/<int:patrocinador__id>", methods=["PUT"])
def updatePatrocinador(patrocinador__id):
    patrocinadoresFound = [patrocinador for patrocinador in patrocinadores if patrocinador["_id"] == patrocinador__id]
    if (len(patrocinadoresFound) > 0):
        patrocinadoresFound[0]["name"] = request.json["name"]
        patrocinadoresFound[0]["href"] = request.json["href"]
        patrocinadoresFound[0]["img_src"] = request.json["img_src"]
        return jsonify({
            "message": "Patrocinador actualizado", "patrocinadores": patrocinadores
        })
    return jsonify({
        "message": "Patrocinador no encontrado"
    })

@app.route("/patrocinadores/<int:patrocinador__id>", methods=["DELETE"])
def deletePatrocinador(patrocinador__id):
    patrocinadoresFound = [patrocinador for patrocinador in patrocinadores if patrocinador["_id"] == patrocinador__id]
    if (len(patrocinadoresFound) > 0):
        
        patrocinadores.remove(patrocinadoresFound[0])
        return jsonify({
            "message": "Patrocinador eliminado", "patrocinadores": patrocinadores
        }) 
    return jsonify({
        "message": "Patrocinador no encontrado"
    })

if __name__ == "__main__":
    app.run()