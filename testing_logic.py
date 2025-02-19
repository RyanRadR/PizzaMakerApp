
import pytest
import toppings_manager, pizza_manager
import moto
import boto3

bkt = "testing-bucket"
reg = "us-east-2"

# Mock data of pizzas.json and toppings.json
mock_toppings_data = {"toppings": ["cheese", "sauce", "onions", "veggies"]}
mock_pizzas_data = {"pizzas": [
    {"name": "pepperoni pizza", "toppings": ["sauce", "cheese", "pepperoni"]},
    {"name": "cheese pizza", "toppings": ["sauce", "cheese"]}]}

@pytest.fixture(autouse=True)
def setup_mock_s3():
    with moto.mock_aws():
        s3 = boto3.client("s3", region_name=reg)
        s3.create_bucket(Bucket=bkt, CreateBucketConfiguration={"LocationConstraint": reg})

        mock_toppings_data = {"toppings": ["cheese", "sauce", "onions", "veggies"]}
        mock_pizzas_data = {"pizzas": [{"name": "cheesepizza", "toppings": ["cheese", "sauce"]}]}

        toppings_manager.save_s3 = lambda x, y: True
        toppings_manager.load_s3 = lambda x : mock_toppings_data
        pizza_manager.save_s3 = lambda x, y: True
        pizza_manager.load_s3 = lambda x : mock_pizzas_data

        yield s3

def test_bkt_exist(setup_mock_s3):
    s3 = setup_mock_s3
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response ["Buckets"]]
    assert bkt in buckets

def test_get_toppings():
    assert toppings_manager.ToppingsManager.get_toppings() == ["cheese", "sauce", "onions", "veggies"]

def test_add_topping():
    assert toppings_manager.ToppingsManager.add_topping("pepperoni") == True
    assert toppings_manager.ToppingsManager.add_topping("cheese") == False  # Duplicate

def test_delete_topping():
    assert toppings_manager.ToppingsManager.delete_topping("cheese") == True
    assert toppings_manager.ToppingsManager.delete_topping("bacon") == False  # Not found

def test_update_topping():
    assert toppings_manager.ToppingsManager.update_topping("veggies", "pepperoni") == True
    assert toppings_manager.ToppingsManager.update_topping("onions", "sauce") == False # Duplicate
    assert toppings_manager.ToppingsManager.update_topping("sausage", "pineapple") == False # Not Found

def test_get_pizza():
    assert pizza_manager.PizzaManager.get_pizzas() == [{"name": "cheesepizza", "toppings": ["cheese", "sauce"]}]

def test_create_pizza():
    assert pizza_manager.PizzaManager.create_pizza("pepperonipizza", ["pepperoni"]) == True
    assert pizza_manager.PizzaManager.create_pizza("cheesepizza", ["cheese", "sauce"]) == False  # Duplicate

def test_delete_pizza():
    assert pizza_manager.PizzaManager.delete_pizza("cheesepizza") == True
    assert pizza_manager.PizzaManager.delete_pizza("meatloverspizza") == False  # Not found

def test_update_pizza():
    assert pizza_manager.PizzaManager.update_pizza_toppings("cheesepizza", ["onion", "sauce"]) == True
    assert pizza_manager.PizzaManager.update_pizza_toppings("cheesepizza", ["sauce", "cheese"]) == True
    assert pizza_manager.PizzaManager.update_pizza_toppings("meatloverspizza", ["sauce", "cheese"]) == False # Not Found
    assert pizza_manager.PizzaManager.update_pizza_name("cheesepizza", "kidspizza") == True

def test_scenario_one():
    #start program
    mock_toppings_data = {}
    mock_pizzas_data = {}
    toppings_manager.save_s3 = lambda x, y: True
    toppings_manager.load_s3 = lambda x : mock_toppings_data
    pizza_manager.save_s3 = lambda x, y: True
    pizza_manager.load_s3 = lambda x : mock_pizzas_data
    #toppings:
    # try listing toppings, should be empty list
    assert toppings_manager.ToppingsManager.get_toppings() == []
    # try removing toppings, return false, b/c no toppings
    assert toppings_manager.ToppingsManager.delete_topping("sauce") == False
    # try changing toppings, return false, b/c no toppings
    assert toppings_manager.ToppingsManager.update_topping("sauce", "cheese") == False
    # try adding sauce, cheese, pepperoni, onions, return true
    assert toppings_manager.ToppingsManager.add_topping("sauce") == True
    assert toppings_manager.ToppingsManager.add_topping("cheese") == True
    assert toppings_manager.ToppingsManager.add_topping("pepperoni") == True
    assert toppings_manager.ToppingsManager.add_topping("onions") == True
    # try listing toppings, should have sauce, cheese, pepperoni, onions
    mock_toppings_data = {"toppings": ["sauce", "cheese", "pepperoni", "onions"]}
    assert toppings_manager.ToppingsManager.get_toppings() == ["sauce", "cheese", "pepperoni", "onions"]
    # try adding sauce, return false, b/c duplicate topping
    assert toppings_manager.ToppingsManager.add_topping("sauce") == False
    # try removing onions, return true
    assert toppings_manager.ToppingsManager.delete_topping("onions") == True
    # try changing pepperoni to sauce, return false, b/c duplicate topping
    assert toppings_manager.ToppingsManager.update_topping("pepperoni", "sauce") == False
    # try changing pepperoni to onion, return true
    assert toppings_manager.ToppingsManager.update_topping("pepperoni", "onions") == True

    #pizza:
    # try listing pizzas, should be empty list
    assert pizza_manager.PizzaManager.get_pizzas() == []
    # try deleting pizza, return false, b/c no pizza
    assert pizza_manager.PizzaManager.delete_pizza("pepperonipizza") == False
    # try updating pizza, return false, b/c no pizza
    assert pizza_manager.PizzaManager.update_pizza_name("pepperonipizza", "cheesepizza") == False
    # try adding cheese pizza with sauce, cheese, onions
    assert pizza_manager.PizzaManager.create_pizza("cheesepizza", ["sauce", "cheese"]) == True
    # try listing pizzas
    mock_pizzas_data = {"pizzas": [{"name": "cheesepizza", "toppings": ["sauce", "cheese"]}]}
    assert pizza_manager.PizzaManager.get_pizzas() == [{"name": "cheesepizza", "toppings": ["sauce", "cheese"]}]
    # try adding cheese pizza, return false, b/c name is same
    assert pizza_manager.PizzaManager.create_pizza("cheesepizza", ["sauce", "cheese", "onions"]) == False
    # try adding kids pizza with sauce, cheese, onions, return false, b/c toppings are same (true b/cc repeat pizza allowed)
    assert pizza_manager.PizzaManager.create_pizza("kidspizza", ["sauce", "cheese", "onions"]) == True
    # try adding kids pizza with sauce, cheese, return true (false b/c repeat names are not allowed on add)
    assert pizza_manager.PizzaManager.create_pizza("kidspizza", ["sauce", "cheese"]) == False
    # try listing pizza, should have cheese pizza, kids pizza
    assert pizza_manager.PizzaManager.get_pizzas() == [{"name": "cheesepizza", "toppings": ["sauce", "cheese"]}, {"name": "kidspizza", "toppings": ["sauce", "cheese", "onions"]}]
    # try deleting kids pizza
    assert pizza_manager.PizzaManager.delete_pizza("kidspizza") == True
    # try updating cheese pizza with sauce, cheese
    assert pizza_manager.PizzaManager.update_pizza_toppings("cheesepizza", ["sauce", "cheese"]) == True
    # try listing pizza, should have cheese pizza
    assert pizza_manager.PizzaManager.get_pizzas() == [{"name": "cheesepizza", "toppings": ["sauce", "cheese"]}, {"name": "kidspizza", "toppings": ["sauce", "cheese", "onions"]}]
