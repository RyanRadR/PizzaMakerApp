
from flask import Flask, request, render_template, redirect, url_for
from pizza_manager import PizzaManager
from toppings_manager import ToppingsManager

app = Flask(__name__)

@app.route("/")
def view_home():
    return render_template("home.html")

@app.route("/toppings", methods=["GET"])
def view_toppings():
    topping_list = ToppingsManager.get_toppings()
    return render_template("toppings.html", toppings=topping_list)

@app.route("/pizzas", methods=["GET"])
def view_pizzas():
    pizza_list = PizzaManager.get_pizzas()
    topping_list = ToppingsManager.get_toppings()
    return render_template("pizzas.html", pizzas=pizza_list, toppings=topping_list)

@app.route("/add-topping", methods=["POST"])
def handle_add_topping():
    topping_name = request.form.get("name")
    ToppingsManager.add_topping(topping_name)
    return redirect(url_for("view_toppings"))

@app.route("/delete-topping", methods=["POST"])
def handle_delete_topping():
    topping_name = request.form.get("name")
    ToppingsManager.delete_topping(topping_name)
    return redirect(url_for("view_toppings"))

@app.route("/update-topping", methods=["POST"])
def handle_update_topping():
    topping_name = request.form.get("name")
    new_topping_name = request.form.get("new-name")
    ToppingsManager.update_topping(topping_name, new_topping_name)
    return redirect(url_for("view_toppings"))

@app.route("/create-pizza", methods=["POST"])
def handle_create_pizza():
    pizza_name = request.form.get("name")
    pizza_toppings = request.form.getlist("toppings")
    PizzaManager.create_pizza(pizza_name, pizza_toppings)
    return redirect(url_for("view_pizzas"))
    
@app.route("/delete-pizza", methods=["POST"])
def handle_delete_pizza():
    pizza_name = request.form.get("name")
    PizzaManager.delete_pizza(pizza_name)
    return redirect(url_for("view_pizzas"))

@app.route("/update-pizza-name", methods=["POST"])
def handle_update_pizza_name():
    pizza_name = request.form.get("name")
    new_pizza_name = request.form.get("new_name")
    PizzaManager.update_pizza_name(pizza_name, new_pizza_name)
    return redirect(url_for("view_pizzas"))

@app.route("/update-pizza-toppings", methods=["POST"])
def handle_update_pizza_toppings():
    pizza_name = request.form.get("name")
    pizza_toppings = request.form.getlist("toppings")
    PizzaManager.update_pizza_toppings(pizza_name, pizza_toppings)
    return redirect(url_for("view_pizzas"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
