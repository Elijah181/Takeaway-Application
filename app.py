from flask import Flask, render_template, request, redirect, url_for
import linecache # import statements to allow flask, buttons, and word files to work

app = Flask(__name__) # important for flask to run
item_list_name_display = []
item_dict_name_amount_display = {}
item_list_description_display = [] 
item_price_list_display = [] # These lists are where the important values are stored
item_find_list = ["bacon_cheeseburger", "chicken_burger", "fish_burger", "cheeseburger", "burger_supreme", "hawaiian_pizza", "meat_lovers_pizza", "peperoni_pizza", "margarita_pizza", "ham_and_cheese_pizza",
                  "fries", "onion_rings", "garlic_bread", "curly_fries", "salad", "fizzy_drink", "lemonade", "milkshake", "orange_juice", "smoothie"]
item_price_list = [10.00, 10.00, 10.00, 9.50, 12.00, 13.00, 13.00, 13.00, 11.00, 11.00, 6.00, 8.00, 5.50, 9.50, 6.00, 3.00, 2.50, 6.00, 2.50, 6.00]
# the item find and item price lists are used to keep track of important values throughout the code
@app.route('/')
def menu():
    return render_template('menu.html') 
    # this route ensures the starts on the menu page
@app.route('/cart')
def cart():
    total_price = 0
    for item in item_price_list_display:
        total_price += item
    return render_template('cart.html', items_name_amount = item_dict_name_amount_display, item_price = item_price_list_display, final_price = total_price)
    # this route allows the user to go from the menu page to the cart and does calculations for the total value of prices
@app.route('/item-to-menu')
def item_to_menu():
    item_list_name_display.pop()
    return render_template("menu.html")
    # takes the user from the individual item pages back to the menu page
    # removes items from the cart as this route is not meant to but items but return without having them in the cart
@app.route('/cart_to_menu')
def cart_to_menu():
    return render_template("menu.html")
    # Takes the user from the cart back to the menu. There is a seperate way to clear cart
@app.route('/checkout_to_menu')
def checkout_to_menu():
    return render_template("menu.html")
    # Takes the user from the checkout to the menu
@app.route('/checkout', methods=['POST'])
def checkout():
    item_list_name_display.clear()
    item_dict_name_amount_display.clear()
    item_list_description_display.clear()
    item_price_list_display.clear()
    return render_template("checkout.html")
    # takes the user from the cart to the checkout and clears all items as they have now been brought
@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    item_list_name_display.clear()
    item_dict_name_amount_display.clear()
    item_list_description_display.clear()
    item_price_list_display.clear()
    return render_template("menu.html")
    # clears users cart and returns them to the menu
@app.route('/process-item', methods=['POST'])
def submit_data():
        global item_index
        form_id = request.form.get('form_id') # this is used to figure out which form is being accessed as there are two within the code
        if form_id == "form_item": # this form is the form which figures out which item the user just brought and how to display it
            received_item_id = request.form.get('item_id') # this line of code works to figure out what menu item was just selected
            if received_item_id in item_find_list:
                item_index = item_find_list.index(received_item_id) # This index is used here and later to keep track of what item was selected
                line_index = item_index + 1
                line_index = line_index * 2 # This calculation works to find where the items are found within the word document
                item_name_display = linecache.getline("words.md", line_index) # this is the name of the item
                item_description_display = linecache.getline("words.md", line_index + 1) # this is the the description of the item
            item_list_description_display.append(item_description_display) 
            item_list_name_display.append(item_name_display)
            return render_template("item.html", items_description = item_list_description_display, items_name = item_list_name_display)
        elif form_id == "form-amount": # this form is the form mainly used for figuring out the amount of a specific item the user ordered
            item_amount = request.form.get("amount", type = int) # getting the item amount
            if item_amount is not None:
                if item_amount <= 0:
                    return render_template("item.html", items_description = item_list_description_display, items_name = item_list_name_display)
                # code used to check boundary cases up above
                else:
                    price = item_price_list[item_index] # figuring out what the price of the selected item should be
                    if item_list_name_display[-1] in item_dict_name_amount_display: # this is for if the item has already been selected and the user wants to increase the amount
                        item_dict_name_amount_display[item_list_name_display[-1]] += item_amount # adds the amount for printing later
                        price_index = list(item_dict_name_amount_display).index(item_list_name_display[-1]) # finds the index of the price to update
                        price *= item_amount # calculates price
                        item_price_list_display[price_index] += price # adds price to value
                    else: # code for new item
                        item_dict_name_amount_display[item_list_name_display[-1]] = item_amount # add item to dictionary
                        price *= item_amount # calculate price
                        item_price_list_display.append(price) # add price
                    return render_template("menu.html") 
            else: # code for boundary cases
                return render_template("item.html", items_description = item_list_description_display, items_name = item_list_name_display)
if __name__ == '__main__':
    app.run(debug=True)
