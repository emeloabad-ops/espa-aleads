from flask import Flask, jsonify, request, send_from_directory
import httpx
import os
import json
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

NEGOCIOS_MUESTRA = [
    {"name": "Bar La Central", "city": "madrid", "category": "bares", "has_website": False, "phone": "+34 620 111 222"},
    {"name": "Peluquería Bella", "city": "barcelona", "category": "peluquerias", "has_website": False, "phone": "+34 630 333 444"},
    {"name": "Restaurante El Sol", "city": "valencia", "category": "restaurantes", "has_website": True, "phone": "+34 611 555 666"},
    {"name": "Fontanería García", "city": "sevilla", "category": "fontaneros", "has_website": False, "phone": "+34 699 777 888"},
    {"name": "Clínica Dental Sonrisa", "city": "madrid", "category": "dentistas", "has_website": True, "phone": "+34 654 999 000"},
    {"name": "Gimnasio FitPro", "city": "barcelona", "category": "gimnasios", "has_website": False, "phone": "+34 612 111 333"},
    {"name": "Electricista Martínez", "city": "malaga", "category": "electricistas", "has_website": False, "phone": "+34 677 444 555"},
    {"name": "Taller Coches Rueda", "city": "bilbao", "category": "talleres", "has_website": False, "phone": "+34 688 222 111"},
    {"name": "Hotel Casa Blanca", "city": "sevilla", "category": "hoteles", "has_website": True, "phone": "+34 954 111 222"},
    {"name": "Tienda Ropa Moda", "city": "zaragoza", "category": "tiendas", "has_website": False, "phone": "+34 976 333 444"},
]

def analizar_negocio(negocio):
    tiene_web = negocio.get("has_website", False)
    if not tiene_web:
        return {
            "score": random.randint(75, 95),
            "pitch": "Este negocio no aparece en Google. Pierde clientes cada dia.",
            "problemas": ["Sin pagina web", "Invisible en Google", "Sin redes sociales"],
            "oportunidades": ["Diseno web", "SEO local", "Google My Business"]
        }
    else:
        return {
            "score": random.randint(40, 65),
            "pitch": "Tiene web pero sin estrategia digital activa.",
            "problemas": ["Web desactualizada", "Sin SEO", "Redes inactivas"],
            "oportunidades": ["Auditoria SEO", "Redes sociales", "Google Ads"]
        }

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/leads")
def get_leads():
    leads = []
    for neg in NEGOCIOS_MUESTRA:
        analisis = analizar_negocio(neg)
        leads.append({
            "name": neg["name"],
            "city": neg["city"],
            "category": neg["category"],
            "score": analisis["score"],
            "pitch": analisis["pitch"],
            "problemas": analisis["problemas"],
            "oportunidades": analisis["oportunidades"],
            "phone": "SOLO SUSCRIPTORES",
            "has_website": neg["has_website"]
        })
    leads.sort(key=lambda x: x["score"], reverse=True)
    return jsonify({"leads": leads, "total": len(leads)})

@app.route("/api/planes")
def get_planes():
    return jsonify({
        "basico":  {"nombre": "Plan Basico",  "precio": 20, "leads": 50},
        "pro":     {"nombre": "Plan Pro",     "precio": 49, "leads": 200},
        "agencia": {"nombre": "Plan Agencia", "precio": 99, "leads": 1000}
    })

if __name__ == "__main__":
    print("Abre en tu navegador: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
