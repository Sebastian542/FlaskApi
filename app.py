from flask import Flask, jsonify, request

app = Flask(__name__)

peliculas = [
    {"id": 1, "titulo": "The Office", "genero": "Comedia", "anio": 2005},
    {"id": 2, "titulo": "Dark", "genero": "Thriller", "anio": 2017}
]

@app.route("/")
def home():
    return "Bienvenido a la API de Películas"

@app.route("/peliculas", methods=["GET"])
def listar():
    return jsonify(peliculas)

@app.route("/peliculas", methods=["POST"])
def agregar():
    nueva = request.get_json()
    peliculas.append(nueva)
    return jsonify(nueva), 201

if __name__ == "__main__":
    app.run(debug=True)
