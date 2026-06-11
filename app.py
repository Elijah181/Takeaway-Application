from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('menu.html')

@app.route('/process-data', methods=['POST'])
def submit_data():

    received_item_id = request.form.get('item_id')
    print(f"Received Item ID: {received_item_id}")
    if received_item_id == "bacon_cheeseburger":
        menu_description = "temporary text"
    return render_template('item.html', description = menu_description)

if __name__ == '__main__':
    app.run(debug=True)
