from flask import Flask, render_template, request, redirect, url_for
import linecache
# import statements to allow flask, buttons, and word files to work

app = Flask(__name__)
item_dict_name_amount_display = {}
item_price_list_display = []
# These lists/dictionaries above are where the important values are stored
item_find_list = ["bacon_cheeseburger", "chicken_burger", "fish_burger",
                  "cheeseburger", "burger_supreme", "hawaiian_pizza",
                  "meat_lovers_pizza", "peperoni_pizza", "margarita_pizza",
                  "ham_and_cheese_pizza", "fries", "onion_rings",
                  "garlic_bread", "curly_fries", "salad", "fizzy_drink",
                  "lemonade", "milkshake", "orange_juice", "smoothie"]
item_price_list = [10.00, 10.00, 10.00, 9.50, 12.00, 13.00, 13.00, 13.00,
                   11.00, 11.00, 6.00, 8.00, 5.50, 9.50, 6.00, 3.00, 2.50,
                   6.00, 2.50, 6.00]
# the lists above are to keep track of important values throughout the code
@app.route('/')
def menu():
    return render_template('menu.html')
    # this route ensures the user starts on the menu page


@app.route('/cart')
def cart():
    global total_price
    total_price = 0
    for item in item_price_list_display:
        total_price += item
    return render_template('cart.html',
                           items_name_amount=item_dict_name_amount_display,
                           item_price=item_price_list_display,
                           final_price=total_price)
    # this route allows the user to go from the menu page to the cart and does calculations for the total value of prices

@app.route('/menu_to_menu')
def menu_to_menu():
    return render_template("menu.html")
# This makes it so when the logo is clicked on the menu page it refreshes so there is consistency across the code
@app.route('/item-to-menu')
def item_to_menu():
    return render_template("menu.html")
    # takes the user from the individual item pages back to the menu page
    # removes items from the cart as this route is not meant to take items but return without having them in the cart
@app.route('/remove-item', methods=['POST'])
def remove_item():
    item_remove = request.form.get("remove")
    # index of item being removed
    item_remove = int(item_remove)
    # set into integer
    item_list = list(item_dict_name_amount_display)
    # convert to dictionary to list
    item_to_remove = item_list[item_remove]
    # use index to find the wanted item
    del item_dict_name_amount_display[item_to_remove]
    # delete item from dictionary
    item_price_list_display.pop(item_remove)
    # remove item from the price list
    total_price = 0
    # reset total price
    for item in item_price_list_display:
        total_price += item
    # calculate total price
    return render_template('cart.html',
                           items_name_amount=item_dict_name_amount_display,
                           item_price=item_price_list_display,
                           final_price=total_price)
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
    item_dict_name_amount_display.clear()
    item_price_list_display.clear()
    return render_template("checkout.html")
    # takes the user from the cart to the checkout and clears all items as they have now been brought
@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    item_dict_name_amount_display.clear()
    item_price_list_display.clear()
    return render_template("menu.html")
    # clears users cart and returns them to the menu
@app.route('/process-item', methods=['POST'])
def submit_data():
    global item_name
    global item_description
    global item_index
    global item_picture
    global item_allergies
    form_id = request.form.get('form_id') # this is used to figure out which form is being accessed as there are two within the code
    if form_id == "form_item": # this form is the form which figures out which item the user just brought and how to display it
            received_item_id = request.form.get('item_id') # this line of code works to figure out what menu item was just selected
            if received_item_id in item_find_list:
                item_index = item_find_list.index(received_item_id) # This index is used here and later to keep track of what item was selected
                line_index = item_index + 1
                line_index = line_index * 4 # This calculation works to find where the items are found within the word document
                item_picture_line = linecache.getline("words.md", line_index)
                item_picture_line = item_picture_line.rstrip('\n')
                item_picture = "/" + item_picture_line + "/" + received_item_id + ".png"
                item_name = linecache.getline("words.md", line_index + 1) # this is the name of the item
                item_description = linecache.getline("words.md", line_index + 2) # this is the the description of the item
                item_allergies = linecache.getline("words.md", line_index + 3)
            return render_template("item.html", items_description_display = item_description, 
                                    items_name_display = item_name, 
                                    items_dict = item_dict_name_amount_display,
                                    item_picture_display = item_picture,
                                    item_allergies_display=item_allergies)
    elif form_id == "form-amount": # this form is the form mainly used for figuring out the amount of a specific item the user ordered
            item_amount = request.form.get("amount", type = int) # getting the item amount
            if item_amount is not None:
                if item_amount <= 0:
                    return render_template("item.html", items_description_display = item_description,
                                            items_name_display = item_name,
                                            items_dict = item_dict_name_amount_display,
                                            item_picture_display = item_picture,
                                            item_allergies_display=item_allergies
                                            )
                # code used to check boundary cases up above
                else:
                    price = item_price_list[item_index] # figuring out what the price of the selected item should be
                    if item_name in item_dict_name_amount_display: # this is for if the item has already been selected and the user wants to increase the amount
                        item_dict_name_amount_display[item_name] += item_amount # adds the amount for printing later
                        price_index = list(item_dict_name_amount_display).index(item_name) # finds the index of the price to update
                        price *= item_amount # calculates price
                        item_price_list_display[price_index] += price # adds price to value
                    else: # code for new item
                        item_dict_name_amount_display[item_name] = item_amount # add item to dictionary
                        price *= item_amount # calculate price
                        item_price_list_display.append(price) # add price
                    return render_template("menu.html") 
            else: # code for boundary cases
                return render_template("item.html", items_description_display = item_description, 
                                       items_name_display = item_name,
                                       items_dict = item_dict_name_amount_display,
                                       item_picture_display = item_picture,
                                       item_allergies_display=item_allergies)
if __name__ == '__main__':
    app.run(debug=True)
