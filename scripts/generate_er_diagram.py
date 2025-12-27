"""
Генерация ER-диаграммы базы данных
"""
from graphviz import Digraph

def create_er_diagram():
    """Создает ER-диаграмму базы данных"""
    
    # Создаем граф
    dot = Digraph(comment='ER-диаграмма БД мебельной компании', format='pdf')
    dot.attr(rankdir='TB', splines='ortho', nodesep='1', ranksep='1.5')
    dot.attr('node', shape='plaintext', fontname='Arial', fontsize='10')
    
    # Таблица Material_types
    material_types = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD BGCOLOR="lightblue" COLSPAN="2"><B>Material_types</B></TD></TR>
        <TR><TD ALIGN="LEFT">🔑 material_type_id</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">material_type_name</TD><TD ALIGN="LEFT">VARCHAR(100)</TD></TR>
        <TR><TD ALIGN="LEFT">waste_percentage</TD><TD ALIGN="LEFT">DECIMAL(5,4)</TD></TR>
        <TR><TD ALIGN="LEFT">description</TD><TD ALIGN="LEFT">TEXT</TD></TR>
        <TR><TD ALIGN="LEFT">is_ecological</TD><TD ALIGN="LEFT">BOOLEAN</TD></TR>
        <TR><TD ALIGN="LEFT">created_at</TD><TD ALIGN="LEFT">TIMESTAMP</TD></TR>
    </TABLE>>'''
    dot.node('Material_types', material_types)
    
    # Таблица Product_types
    product_types = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD BGCOLOR="lightblue" COLSPAN="2"><B>Product_types</B></TD></TR>
        <TR><TD ALIGN="LEFT">🔑 product_type_id</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">product_type_name</TD><TD ALIGN="LEFT">VARCHAR(100)</TD></TR>
        <TR><TD ALIGN="LEFT">type_coefficient</TD><TD ALIGN="LEFT">DECIMAL(5,2)</TD></TR>
        <TR><TD ALIGN="LEFT">style</TD><TD ALIGN="LEFT">VARCHAR(50)</TD></TR>
        <TR><TD ALIGN="LEFT">description</TD><TD ALIGN="LEFT">TEXT</TD></TR>
        <TR><TD ALIGN="LEFT">created_at</TD><TD ALIGN="LEFT">TIMESTAMP</TD></TR>
    </TABLE>>'''
    dot.node('Product_types', product_types)
    
    # Таблица Workshops
    workshops = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD BGCOLOR="lightblue" COLSPAN="2"><B>Workshops</B></TD></TR>
        <TR><TD ALIGN="LEFT">🔑 workshop_id</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">workshop_name</TD><TD ALIGN="LEFT">VARCHAR(100)</TD></TR>
        <TR><TD ALIGN="LEFT">workshop_type</TD><TD ALIGN="LEFT">VARCHAR(100)</TD></TR>
        <TR><TD ALIGN="LEFT">staff_count</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">location</TD><TD ALIGN="LEFT">VARCHAR(200)</TD></TR>
        <TR><TD ALIGN="LEFT">equipment_description</TD><TD ALIGN="LEFT">TEXT</TD></TR>
        <TR><TD ALIGN="LEFT">is_active</TD><TD ALIGN="LEFT">BOOLEAN</TD></TR>
        <TR><TD ALIGN="LEFT">created_at</TD><TD ALIGN="LEFT">TIMESTAMP</TD></TR>
    </TABLE>>'''
    dot.node('Workshops', workshops)
    
    # Таблица Products
    products = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD BGCOLOR="lightgreen" COLSPAN="2"><B>Products</B></TD></TR>
        <TR><TD ALIGN="LEFT">🔑 product_id</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">product_name</TD><TD ALIGN="LEFT">VARCHAR(200)</TD></TR>
        <TR><TD ALIGN="LEFT">article_number</TD><TD ALIGN="LEFT">VARCHAR(50)</TD></TR>
        <TR><TD ALIGN="LEFT">🔗 product_type_id</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">🔗 material_type_id</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">min_partner_price</TD><TD ALIGN="LEFT">DECIMAL(10,2)</TD></TR>
        <TR><TD ALIGN="LEFT">dimensions</TD><TD ALIGN="LEFT">VARCHAR(100)</TD></TR>
        <TR><TD ALIGN="LEFT">weight</TD><TD ALIGN="LEFT">DECIMAL(8,2)</TD></TR>
        <TR><TD ALIGN="LEFT">description</TD><TD ALIGN="LEFT">TEXT</TD></TR>
        <TR><TD ALIGN="LEFT">is_available</TD><TD ALIGN="LEFT">BOOLEAN</TD></TR>
        <TR><TD ALIGN="LEFT">created_at</TD><TD ALIGN="LEFT">TIMESTAMP</TD></TR>
        <TR><TD ALIGN="LEFT">updated_at</TD><TD ALIGN="LEFT">TIMESTAMP</TD></TR>
    </TABLE>>'''
    dot.node('Products', products)
    
    # Таблица Product_workshops
    product_workshops = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD BGCOLOR="lightyellow" COLSPAN="2"><B>Product_workshops</B></TD></TR>
        <TR><TD ALIGN="LEFT">🔑 product_workshop_id</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">🔗 product_id</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">🔗 workshop_id</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">production_time_hours</TD><TD ALIGN="LEFT">DECIMAL(6,2)</TD></TR>
        <TR><TD ALIGN="LEFT">priority</TD><TD ALIGN="LEFT">INT</TD></TR>
        <TR><TD ALIGN="LEFT">notes</TD><TD ALIGN="LEFT">TEXT</TD></TR>
        <TR><TD ALIGN="LEFT">created_at</TD><TD ALIGN="LEFT">TIMESTAMP</TD></TR>
    </TABLE>>'''
    dot.node('Product_workshops', product_workshops)
    
    # Связи
    dot.edge('Product_types', 'Products', label='1:N', fontsize='9', 
             arrowhead='crow', arrowtail='none', dir='both')
    dot.edge('Material_types', 'Products', label='1:N', fontsize='9',
             arrowhead='crow', arrowtail='none', dir='both')
    dot.edge('Products', 'Product_workshops', label='1:N', fontsize='9',
             arrowhead='crow', arrowtail='none', dir='both')
    dot.edge('Workshops', 'Product_workshops', label='1:N', fontsize='9',
             arrowhead='crow', arrowtail='none', dir='both')
    
    # Сохраняем
    dot.render('ER_diagram', cleanup=True)
    print("ER-диаграмма создана: ER_diagram.pdf")

if __name__ == "__main__":
    create_er_diagram()
