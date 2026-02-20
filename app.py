from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# База даних товарів (поки що просто список)
products = [
    {"id": 1, "name": "Собача іграшка", "price": 150},
    {"id": 2, "name": "Корм для котів", "price": 200}
]

cart = []

# Головна сторінка
@app.route("/")
def home():
    return render_template("index.html", products=products)

# Сторінка товару
@app.route("/product/<int:product_id>")
def product(product_id):
    product_item = next((p for p in products if p["id"] == product_id), None)
    return render_template("product.html", product=product_item)

# Додати товар у кошик
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product_item = next((p for p in products if p["id"] == product_id), None)
    if product_item:
        cart.append(product_item)
    return redirect(url_for("cart_page"))

# Кошик
@app.route("/cart")
def cart_page():
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

# Кабінет продавця
@app.route("/admin")
def admin():
    return render_template("admin.html", products=products)

# Додати товар через форму
@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        new_id = max([p["id"] for p in products] + [0]) + 1
        name = request.form.get("name")
        price = float(request.form.get("price"))
        products.append({"id": new_id, "name": name, "price": price})
        return redirect(url_for("admin"))
    return render_template("add_product.html")

if __name__ == "__main__":
    app.run(debug=True)
