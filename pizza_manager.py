
from s3 import load_s3, save_s3

class PizzaManager:
    file_name = "pizzas.json"

    # get_pizzas() loads pizzas data from AWS cloud file
    @staticmethod
    def get_pizzas():
        data = load_s3(PizzaManager.file_name)
        return data["pizzas"] if data else []

    # create_pizza() creates a pizza given a name and list of toppings if pizza name does not exist
    @staticmethod
    def create_pizza(name, toppings):
        pizzas = PizzaManager.get_pizzas()
        if any(p["name"] == name for p in pizzas):
            print(f"{name} already exists.")
            return False
        new_pizza = {"name": name, "toppings": toppings}
        pizzas.append(new_pizza)
        save_s3(PizzaManager.file_name, {"pizzas": pizzas})
        print(f"{name} added")
        return True

    # delete_pizza() is used to delete a pizza using its name
    @staticmethod
    def delete_pizza(name):
        pizzas = PizzaManager.get_pizzas()
        if not any(p["name"] == name for p in pizzas):
            print(f"{name} not found.")
            return False
        updated_pizzas = [p for p in pizzas if p["name"] != name]
        save_s3(PizzaManager.file_name, {"pizzas": updated_pizzas})
        print(f"{name} deleted")
        return True

    # update_pizza_name updates name of pizza with new name if name exists
    @staticmethod
    def update_pizza_name(name, new_name):
        pizzas = PizzaManager.get_pizzas()
        for pizza in pizzas:
            if pizza["name"] == name:
                pizza["name"] = new_name
                save_s3(PizzaManager.file_name, {"pizzas": pizzas})
                print(f"{name} updated to {new_name}")
                return True
        print(f"{name} not found.")
        return False
    
    # update_pizza_topping takes pizza name and updates toppings
    @staticmethod
    def update_pizza_toppings(name, new_toppings):
        pizzas = PizzaManager.get_pizzas()
        for pizza in pizzas:
            if pizza["name"] == name:
                pizza["toppings"] = new_toppings
                save_s3(PizzaManager.file_name, {"pizzas": pizzas})
                print(f"{name} updated with {new_toppings}")
                return True
        print(f"{name} not found.")
        return False

