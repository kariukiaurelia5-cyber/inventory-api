import requests

BASE_URL = "http://127.0.0.1:5000"


def menu():
    while True:
        print("\n==== INVENTORY MENU ====")
        print("1. View Inventory")
        print("2. Add Item")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Fetch Product from API")
        print("6. Add Product from API")
        print("7. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            res = requests.get(f"{BASE_URL}/inventory")
            print(res.json())

        elif choice == "2":
            name = input("Product name: ")
            price = float(input("Price: "))
            stock = int(input("Stock: "))

            data = {
                "product_name": name,
                "price": price,
                "stock": stock
            }

            res = requests.post(f"{BASE_URL}/inventory", json=data)
            print(res.json())

        elif choice == "3":
            item_id = input("Item ID: ")
            new_price = float(input("New price: "))

            res = requests.patch(
                f"{BASE_URL}/inventory/{item_id}",
                json={"price": new_price}
            )
            print(res.json())

        elif choice == "4":
            item_id = input("Item ID: ")
            res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
            print(res.json())

        elif choice == "5":
            barcode = input("Enter barcode: ")
            res = requests.get(f"{BASE_URL}/fetch/{barcode}")
            print(res.json())

        elif choice == "6":
            barcode = input("Enter barcode: ")
            res = requests.post(f"{BASE_URL}/add-from-api/{barcode}")
            print(res.json())

        elif choice == "7":
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    menu()