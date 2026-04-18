from flask import Flask, jsonify, send_from_directory
import os
import random

app = Flask(__name__, static_folder="static")

NEGOCIOS = [
    {"name": "Bar La Central", "city": "madrid", "category": "bares", "has_website": False},
    {"name": "Peluqueria Bella", "city": "barcelona", "category": "peluquerias", "has_website": False},
    {"name": "Restaurante El Sol", "city": "valencia", "category": "restaurantes", "has_website": True},
    {"name": "Fontaneria Garcia", "city": "sevilla", "category": "fontaneros", "has_website": False},
    {"name": "Clinica Dental Sonrisa", "city": "madrid", "category": "dentistas", "has_website": True},
    {"name": "Gimnasio FitPro", "city": "barcelona", "category": "gimnasios", "has_website": False},
    {"name": "Electricista Martinez", "city": "malaga", "category": "electricistas", "has_website": False},
    {"name": "Taller Coches Rueda", "city": "bilbao", "category": "talleres", "has_website": False},
    {"name": "Hotel Casa Blanca", "city": "sevilla", "category": "hoteles", "has_website": True},
    {"name": "Tienda Ropa Moda", "city": "zaragoza", "category": "tiendas", "has_website": False},
]

def analizar(n):
    if not n.get("has_website"):
        return {"score": random.randint(75, 95), "pitch": "Sin web. Pierde clientes cada dia."}
    return {"score": random.randint(40, 65), "pitch": "Tiene web pero sin estrategia digital."}

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/leads")
def get_leads():
    leads = []
    for n in NEGOCIOS:
        a = analizar(n)
        leads.append({"name": n["name"], "city": n["city"], "category": n["category"], "score": a["score"], "pitch": a["pitch"], "phone": "SOLO SUSCRIPTORES"})
    leads.sort(key=lambda x: x["score"], reverse=True)
    return jsonify({"leads": leads, "total": len(leads)})

@app.route("/api/planes")
def get_planes():
    return jsonify({"basico": {"precio": 20}, "pro": {"precio": 49}, "agencia": {"precio": 99}})
