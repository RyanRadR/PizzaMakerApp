
from s3 import load_s3, save_s3

class ToppingsManager:
    file_name = "toppings.json"

    # get_toppings() loads toppings data from AWS cloud file
    @staticmethod
    def get_toppings():
        data = load_s3(ToppingsManager.file_name)
        return data["toppings"] if data else []
    
    # add_toppings() adds a topping to list if topping is not in list
    @staticmethod
    def add_topping(topping):
        toppings = ToppingsManager.get_toppings()
        if topping not in toppings:
            toppings.append(topping)
            save_s3(ToppingsManager.file_name, {"toppings": toppings})
            print(f"{topping} added")
            return True
        print(f"{topping} already exists")
        return False

    # delete_topping() removes topping from list if the topping exists in the list
    @staticmethod
    def delete_topping(topping):
        toppings = ToppingsManager.get_toppings()
        if topping in toppings:
            toppings.remove(topping)
            save_s3(ToppingsManager.file_name, {"toppings": toppings})
            print(f"{topping} deleted")
            return True
        print(f"{topping} not found")
        return False
    
    # update_topping() removes topping if in list and then adds new topping if it exists
    @staticmethod
    def update_topping(topping, new_topping):
        toppings = ToppingsManager.get_toppings()
        if topping in toppings:
            toppings.remove(topping)
            if new_topping not in toppings:
                toppings.append(new_topping)
                save_s3(ToppingsManager.file_name, {"toppings": toppings})
                print(f"{topping} replaced with {new_topping}")
                return True
            else:
                print(f"{new_topping} is a duplicate")
                toppings.append(topping)
        else:
            print(f"{topping} not found")
        return False

