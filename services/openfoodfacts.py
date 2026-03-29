import requests

def fetch_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data.get("status") == 1:
                product = data.get("product", {})

                return {
                    "product_name": product.get("product_name", "Unknown"),
                    "brand": product.get("brands", "Unknown"),
                    "ingredients": product.get("ingredients_text", "Not available")
                }

    except Exception as e:
        print("Error fetching product:", e)

    return None