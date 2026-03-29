from unittest.mock import patch
from services.openfoodfacts import fetch_product


@patch('services.openfoodfacts.requests.get')
def test_fetch_product(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mock Milk",
            "brands": "Mock Brand",
            "ingredients_text": "Water"
        }
    }

    result = fetch_product("123")
    assert result["product_name"] == "Mock Milk"