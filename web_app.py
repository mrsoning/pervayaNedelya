# веб приложение для мебельной компании
from flask import Flask, render_template, request, redirect, url_for, jsonify
from scripts.db_manager_sqlite import DatabaseManager
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'furniture-company-secret-key'

# Инициализация БД
db = DatabaseManager()

@app.route('/')
def index():
    # главная страница
    stats = db.get_statistics()
    return render_template('index.html', stats=stats)

@app.route('/products')
def products():
    # список продукции
    search = request.args.get('search', '')
    
    if search:
        products_list = db.search_products(search)
    else:
        products_list = db.get_products()
    
    return render_template('products.html', products=products_list, search=search)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    # добавить продукцию
    if request.method == 'POST':
        name = request.form['name']
        article = request.form['article']
        product_type_id = request.form['product_type_id']
        material_type_id = request.form['material_type_id']
        price = request.form['price']
        
        db.add_product(name, article, product_type_id, material_type_id, price)
        return redirect(url_for('products'))
    
    product_types = db.get_product_types()
    material_types = db.get_material_types()
    
    return render_template('add_product.html', 
                         product_types=product_types,
                         material_types=material_types)

@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # редактировать продукцию
    if request.method == 'POST':
        updates = {
            'product_name': request.form['name'],
            'min_partner_price': request.form['price'],
            'is_available': 1 if request.form.get('is_available') else 0
        }
        db.update_product(product_id, **updates)
        return redirect(url_for('products'))
    
    product = db.execute_query("SELECT * FROM Products WHERE product_id = ?", (product_id,))
    if product:
        product = product[0]
    
    return render_template('edit_product.html', product=product)

@app.route('/products/delete/<int:product_id>')
def delete_product(product_id):
    # удалить продукцию
    db.delete_product(product_id)
    return redirect(url_for('products'))

@app.route('/workshops')
def workshops():
    # список цехов
    workshops_list = db.get_workshops()
    return render_template('workshops.html', workshops=workshops_list)

@app.route('/analytics')
def analytics():
    # аналитика
    by_type = db.get_products_by_type()
    avg_price = db.get_average_price_by_type()
    top_products = db.get_top_expensive_products(10)
    
    return render_template('analytics.html',
                         by_type=by_type,
                         avg_price=avg_price,
                         top_products=top_products)

@app.route('/api/stats')
def api_stats():
    # апи статистика
    return jsonify(db.get_statistics())

@app.route('/api/products')
def api_products():
    # апи продукция
    return jsonify(db.get_products())

if __name__ == '__main__':
    # Создать папку templates если нет
    Path('templates').mkdir(exist_ok=True)
    
    print("\n" + "="*60)
    print("  ВЕБ-ПРИЛОЖЕНИЕ: БД МЕБЕЛЬНОЙ КОМПАНИИ")
    print("="*60)
    print("\n  Откройте в браузере: http://127.0.0.1:5000")
    print("\n  Нажмите Ctrl+C для остановки\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
