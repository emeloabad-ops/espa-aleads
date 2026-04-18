from flask import Flask, jsonify, send_from_directory, request
import os
import random
import httpx

app = Flask(__name__, static_folder="static")

NOWPAYMENTS_API_KEY = "95VRNJ7-199MPQJ-J1W8HS3-6C8RGW1"
WALLET = "TW8BgZkMGK7DnP7CycXssnPWa2tHPCFdDE"

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

PLANES = {
    "basico": {"nombre": "Plan Basico", "precio": 20, "leads": 50},
    "pro": {"nombre": "Plan Pro", "precio": 49, "leads": 200},
    "agencia": {"nombre": "Plan Agencia", "precio": 99, "leads": 1000}
}

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

@app.route("/api/pagar", methods=["POST"])
def crear_pago():
    data = request.json
    plan = data.get("plan", "basico")
    email = data.get("email", "")
    if plan not in PLANES:
        return jsonify({"error": "Plan no valido"}), 400
    precio = PLANES[plan]["precio"]
    try:
        response = httpx.post(
            "https://api.nowpayments.io/v1/payment",
            headers={"x-api-key": NOWPAYMENTS_API_KEY, "Content-Type": "application/json"},
            json={
                "price_amount": precio,
                "price_currency": "usd",
                "pay_currency": "usdttrc20",
                "payout_address": WALLET,
                "order_description": f"{email}|{plan}",
                "ipn_callback_url": "https://shodky99.pythonanywhere.com/api/webhook/nowpayments"
            },
            timeout=30
        )
        result = response.json()
        if "payment_id" in result:
            return jsonify({"success": True, "pay_address": result["pay_address"], "pay_amount": result["pay_amount"]})
        return jsonify({"error": result}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/webhook/nowpayments", methods=["POST"])
def webhook():
    data = request.json
    if data.get("payment_status") == "finished":
        print(f"PAGO CONFIRMADO: {data.get('order_description')}")
    return jsonify({"status": "ok"})

@app.route("/api/planes")
def get_planes():
    return jsonify(PLANES)
