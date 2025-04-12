from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
jwt = JWTManager(app)
swagger = Swagger(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    ingredient = db.Column(db.Text, nullable=False)
    time_minutes = db.Column(db.Integer, nullable=False)

@app.route("/register", methods=["POST"])
def register_user():
    """
    Registra um novo usuario.
    ---
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
                username:
                    type: string
                password:
                    type: string
    responses:
        201:
          description: Usuario criado com sucesso
        400:
          description: Usuario ja existe
    """
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 400
    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201

@app.route("/login", methods=["POST"])
def login():
    """
    Faz login do usuario e retorna um JWT.
    ---
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
                username:
                    type: string
                password:
                    type: string
    responses:
        201:
          description: Login bem sucedido, retorna JWT
        400:
          description: Credenciais invalidas
    """
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.password == data["password"]:
        token = create_access_token(identity=str(user.id))
        return jsonify({"acess_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"msg": f"Usuario com ID {current_user_id} acessou a rota protegida"}), 200


@app.route("/recipes", methods=["POST"])
@jwt_required()
def create_recipe():
    """
    Cria uma nova receita.
    ---
    security:
        - BearerAuth: []
    parameter:
        - in: body
          name: body
          schema:
            type: object
            required: true
            properties:
                title:
                    type: string
                ingredient:
                    type: string
                time_minutes:
                    type: string
    """
    data = request.get_json()
    new_recipe = Recipe(
        title= data["title"],
        ingredient= data["ingredient"],
        time_minutes = data["time_minutes"]
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"msg": "Recipe created"}), 201


@app.route("/recipes", methods=["GET"])
def get_recipes():
    """
    Lista receitas com filtros opcionais.
    ---
    parameters:
        - in: query
          name: ingredient
          type: string
          required: true
          description: Filtra por ingrediente
        - in: query
          name: max_time
          type: integer
          required: false
          description: Tempo maximo de preparo (minutos)
    responses:
        200:
            description: Lista de receitas filtradas
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                        title:
                            type: string
                        time_minutes:
                            type: integer
    """
    ingredient = request.args.get("ingredient")
    max_time = request.args.get("max_time", type=int)

    query = Recipe.query
    if ingredient:
        query = query.filter(Recipe.ingredient.ilike(f"{ingredient}"))
    if max_time is not None:
        query = query.filter(Recipe.time_minutes <= max_time)

    recipes = query.all()
    return jsonify([
        {
        "id": r.id,
        "title": r.title,
        "ingredient": r.ingredient,
        "time_minutes": r.time_minutes
        }
    for r in recipes]
    )

@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
@jwt_required
def update_recipe(recipe_id):
    """
    Atualiza uma receita existente.
    ---
    security:
        - BearerAuth: []
    parameters:
        - in: path
           name: recipe_id
           required: true
           type: integer
        - in: body
          name: body
          schema:
            type: object
            properties:
                title: string
            ingredientes:
                type: string
            time_minutes:
                type: integer
    responses:
        200:
            description: Receita atualizada
        404:
            description: Receita nao encontrada
        401:
            description: token nao fornecido ou invalido
    """
    data = request.get_json()
    recipe = Recipe.query.get_or_404(recipe_id)
    if "title" in data:
        recipe.title = data["title"]
    if "ingredientes" in data:
        recipe.ingredient = data["ingredientes"]
    if "time_minutes" in data:
        recipe.time_minutes = data["time_minutes"]

    df.session.commit()
    return jsonify({"msg": "Recipe updated"}), 200


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    #     print("Banco de dados criado!")
    app.run(debug=True)

    
