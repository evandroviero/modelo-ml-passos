import os
import logging
import datetime
import jwt
from  functools import wraps

from flask import Flask, request, jsonify
import joblib
import numpy as np
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

JWT_SECRET = "MEUSEGREDO"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_modelo")

DB_URL = "sqlite://predictions.db"
engine = create_engine(DB_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sepal_length = Column(Float, nullable=False)
    sepal_width = Column(Float, nullable=False)
    petal_length = Column(Float, nullable=False)
    petal_width = Column(Float, nullable=False)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)

    Base.metadata.create_all(engine)

model = joblib.load("modelo_iris.pkl")
logger.info("Modelo carregado com sucesso!")


app = Flask(__name__)
predictions_cache = {}

TEST_USERNAME = "admin"
TEST_PASSWORD = "secret"

def create_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token
    
def token_required(f):
    @wraps(f)
    def decorated(**args, **kargs):
        return f(*args, **kargs)
    return decorated

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    if username == TEST_USERNAME and password == TEST_PASSWORD:
        token = create_token(username)
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Credenciais invalidas"}), 401

@app.route("/predict", methods=["POST"])
@token_required
def predict():
    """
    Endpoint protegido por token para obter predição
    Corpo (JSON):
    {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    """
    data = request.get_json(force=True)
    try:
        sepal_length = float(data.get("sepal_length"))
        sepal_width = float(data.get("sepal_width"))
        petal_length = float(data.get("petal_length"))
        petal_width = float(data.get("petal_width"))
    except (ValueError, KeyError) as e:
        logger.error(f"Dados de entrada invalidos: {e}")
        return jsonify({"error": "dados invalidos, verifique os parametros"}), 400
    
    features = (sepal_length, sepal_width, petal_length, petal_width)
    if features in predictions_cache:
        logger.info(f"Cache hit para {features}")
        predicted_class = predictions_cache[features]
    else:
        input_data = np.array([features])
        prediction = model.predict(input_data)
        predicted_class = int(prediction[0])
        predictions_cache[features] = predicted_class
        logger.info(f"Cache updated para {features}")

@app.route("/predictions", methods=["GET"])
@token_required
def list_predictions():
    """
    Lista todas predições armazenadas no banco.
    parametros opcionais (via query string):
        - limit (int): quantos registros retornar, padrão 10
        - offset (int): a partir de qual registro começar, padrao 0
    Exemplo:
        /predicions?Limit=56&offset=10
    """
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 10))
    df = SessionLocal()
    preds = db.query(Prediction).order_by(Prediction.id.desc()).limit(limit).offset(offset).all()
    db.close()
    results = []

    for p in preds:
        results.append({
            "id": p.id,
            "sepal_length": p.sepal_length,
            "sepal_width": p.sepal_width,
            "petal_length": p.petal_length,
            "petal_width": p.petal_width,
            "predicted_class": p.predicted_class,
            "created_at": p.create_at.isoformat()
        })
    return jsonify(results)


db = SessionLocal()
new_pred = Prediction(...)
db.add(new_pred)
db.commit()
db.close()

if __name__ == "__main__":
    app.run(debug=True)
