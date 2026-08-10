from flask import Flask, render_template, request, redirect, url_for
import linecache

app = Flask(__name__)
item_list_name_display = []
item_dict_name_amount_display = {}
item_list_description_display = []
item_find_list = ["bacon_cheeseburger", "chicken_burger", "fish_burger", "cheeseburger", "burger_supreme", "hawaiian_pizza", "meat_lovers_pizza", "peperoni_pizza", "margarita_pizza", "ham_and_cheese_pizza",
                  "fries", "onion_rings", "garlic_bread", "curly_fries", "salad", "fizzy_drink", "lemonade", "milkshake", "orange_juice", "smoothie"]
item_price_list = [10.00, 10.00, 10.00, 9.50, 12.00, 13.00, 13.00, 13.00, 11.00, 11.00, 6.00, 8.00, 5.50, 9.50, 6.00, 3.00, 2.50, 6.00, 2.50, 6.00]
item_price_list_display = []
@app.route('/')
def menu():
    return render_template('menu.html')
@app.route('/cart')
def cart():
    total_price = 0
    for item in item_price_list_display:
        total_price += item
    return render_template('cart.html', items_name_amount = item_dict_name_amount_display, item_price = item_price_list_display, final_price = total_price)
@app.route('/item-to-menu')
def item_to_menu():
    item_list_name_display.pop()
    return render_template("menu.html")
@app.route('/cart_to_menu')
def cart_to_menu():
    return render_template("menu.html")
@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    item_list_name_display.clear()
    item_dict_name_amount_display.clear()
    item_list_description_display.clear()
    item_price_list_display.clear()
    return render_template("menu.html")
@app.route('/process-item', methods=['POST'])
def submit_data():
        global item_index
        form_id = request.form.get('form_id')
        if form_id == "form_item":
            received_item_id = request.form.get('item_id')
            if received_item_id in item_find_list:
                item_index = item_find_list.index(received_item_id)
                line_index = item_index + 1
                line_index = line_index * 2
                item_name_display = linecache.getline("words.md", line_index)
                item_description_display = linecache.getline("words.md", line_index + 1)
            item_list_description_display.append(item_description_display)
            item_list_name_display.append(item_name_display)
            return render_template("item.html", items_description = item_list_description_display, items_name = item_list_name_display)
        elif form_id == "form-amount":
            item_amount = request.form.get("amount", type = int)
            if item_amount is not None:
                if item_amount <= 0:
                    return render_template("item.html", items_description = item_list_description_display, items_name = item_list_name_display)
                else:
                    price = item_price_list[item_index]
                    if item_list_name_display[-1] in item_dict_name_amount_display:
                        item_dict_name_amount_display[item_list_name_display[-1]] += item_amount
                        price_index = list(item_dict_name_amount_display).index(item_list_name_display[-1])
                        price *= item_amount
                        item_price_list_display[price_index] += price
                    else:
                        item_dict_name_amount_display[item_list_name_display[-1]] = item_amount
                        price *= item_amount
                        item_price_list_display.append(price)
                    return render_template("menu.html") 
            else:
                return render_template("item.html", items_description = item_list_description_display, items_name = item_list_name_display)
if __name__ == '__main__':
    app.run(debug=True)
