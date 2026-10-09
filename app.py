from flask import Flask, jsonify, request
import math

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "nazwa": "Klawiatura mechaniczna", "kategoria": "akcesoria", "cena": 349.99, "opis": "Przełączniki hot-swap, podświetlenie RGB"},
    {"id": 2, "nazwa": "Mysz bezprzewodowa", "kategoria": "akcesoria", "cena": 129.00, "opis": "Ciche przyciski, 4000 DPI"},
    {"id": 3, "nazwa": "Monitor 27 cali", "kategoria": "monitory", "cena": 1099.00, "opis": "Matryca IPS, 144 Hz"},
    {"id": 4, "nazwa": "Słuchawki nauszne", "kategoria": "audio", "cena": 449.00, "opis": "ANC, 40 h pracy na baterii"},
    {"id": 5, "nazwa": "Hub USB-C", "kategoria": "akcesoria", "cena": 199.00, "opis": "HDMI, 3x USB-A, czytnik SD"},
]

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/products")
def products():
    if "max_price" not in request.args:
        return jsonify(PRODUCTS)

    max_price = request.args.get("max_price", type=float)

    if max_price is None or not math.isfinite(max_price) or max_price < 0:
        return jsonify({"error": "invalid max_price"}), 400

    filtered = [
        p for p in PRODUCTS
        if p["cena"] <= max_price
    ]

    return jsonify(filtered)

@app.route("/api/products/<int:product_id>")
def product(product_id):
    item = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if item is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(item)

@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON must be an object"}), 400

    if "id" in data:
        return jsonify({"error": "id is assigned by server"}), 400

    required = ["nazwa", "kategoria", "opis", "cena"]

    if any(field not in data for field in required):
        return jsonify({"error": "missing required field"}), 400

    for field in ["nazwa", "kategoria", "opis"]:
        if not isinstance(data[field], str) or not data[field].strip():
            return jsonify({"error": f"invalid field: {field}"}), 400

    cena = data["cena"]

    if (
        isinstance(cena, bool)
        or not isinstance(cena, (int, float))
        or not math.isfinite(cena)
        or cena < 0
    ):
        return jsonify({"error": "invalid cena"}), 400

    new_id = max((p["id"] for p in PRODUCTS), default=0) + 1

    new_product = {
        "id": new_id,
        "nazwa": data["nazwa"],
        "kategoria": data["kategoria"],
        "opis": data["opis"],
        "cena": cena
    }

    PRODUCTS.append(new_product)

    return jsonify(new_product), 201

if __name__ == "__main__":
    app.run(debug=True)