from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/item')
def item():
    return render_template('item.html')

@app.route('/process-item', methods=['POST'])
def submit_data():
        form_id = request.form.get('form_id')
        if form_id == "form_item":
            received_item_id = request.form.get('item_id')
            if received_item_id == "bacon_cheeseburger":
                item_description = "bacon cheesburger"
            elif received_item_id == "chicken_burger":
                item_description = "chicken burger"
            elif received_item_id == "fish_burger":
                item_description = "fish burger"
            elif received_item_id == "cheeseburger":
                item_description = "cheeseburger"
            elif received_item_id == "burger_supreme":
                item_description = "burger supreme"
            elif received_item_id == "chicken_burger":
                item_description = "chicken burger"
            elif received_item_id == "hawaiian_pizza":
                item_description = "hawaiian pizza"
            elif received_item_id == "meat_lovers_pizza":
                item_description = "meat lovers pizza"
            elif received_item_id == "peperoni_pizza":
                item_description = "peperoni pizza"
            elif received_item_id == "margarita_pizza":
                item_description = "margarita pizza"
            elif received_item_id == "ham_and_cheese_pizza":
                item_description = "ham and cheese pizza"
            elif received_item_id == "fries":
                item_description = "fries"
            elif received_item_id == "onion_rings":
                item_description = "onion rings"
            elif received_item_id == "garlic_bread":
                item_description = "garlic bread"
            elif received_item_id == "curly_fries":
                item_description == "curly fries"
            elif received_item_id == "salad":
                item_description == "salad"
            elif received_item_id == "fizzy_drink":
                item_description = "fizzy drink"
            elif received_item_id == "lemonade":
                item_description = "lemonade"
            elif received_item_id == "orange_juice":
                item_description = "orange juice"
            elif received_item_id == "milkshake":
                item_description = "milkshake"
            elif received_item_id == "smoothie":
                item_description = "smoothie"
            return redirect(url_for("item"))
if __name__ == '__main__':
    app.run(debug=True)
