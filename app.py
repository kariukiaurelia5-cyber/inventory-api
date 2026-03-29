from flask import Flask, request, jsonify
from database import inventory, current_id
from services.openfoodfacts import fetch_product

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Inventory API is running"}

# GET ALL
@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)


# GET ONE
@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


# CREATE
@app.route('/inventory', methods=['POST'])
def add_item():
    global current_id
    data = request.json

    if not data.get("product_name"):
        return jsonify({"error": "Product name required"}), 400

    item = {
        "id": current_id,
        "product_name": data.get("product_name"),
        "brand": data.get("brand", "Unknown"),
        "price": data.get("price", 0),
        "stock": data.get("stock", 0),
        "ingredients": data.get("ingredients", "")
    }

    inventory.append(item)
    current_id += 1

    return jsonify(item), 201


# UPDATE
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.json

    for item in inventory:
        if item["id"] == item_id:
            item.update(data)
            return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


# DELETE
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return jsonify({"message": "Item deleted"})

    return jsonify({"error": "Item not found"}), 404


# FETCH FROM EXTERNAL API
@app.route('/fetch/<barcode>', methods=['GET'])
def fetch_external(barcode):
    product = fetch_product(barcode)

    if product:
        return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


# BONUS: Add item directly from API
@app.route('/add-from-api/<barcode>', methods=['POST'])
def add_from_api(barcode):
    global current_id
    product = fetch_product(barcode)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    item = {
        "id": current_id,
        "product_name": product["product_name"],
        "brand": product["brand"],
        "price": 0,
        "stock": 0,
        "ingredients": product["ingredients"]
    }

    inventory.append(item)
    current_id += 1

    return jsonify(item), 201


if __name__ == '__main__':
    app.run(debug=True)