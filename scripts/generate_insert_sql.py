"""
Генерация SQL INSERT запросов из CSV файлов
"""
import pandas as pd
import os

def escape_sql_string(value):
    """Экранирует строку для SQL"""
    if pd.isna(value):
        return 'NULL'
    if isinstance(value, str):
        return "'" + str(value).replace("'", "''") + "'"
    return str(value)

def generate_inserts():
    """Генерирует SQL INSERT запросы"""
    
    sql_output = []
    sql_output.append("-- =============================================")
    sql_output.append("-- Импорт данных в базу данных")
    sql_output.append("-- =============================================\n")
    
    # 1. Material_types
    sql_output.append("-- =============================================")
    sql_output.append("-- Импорт типов материалов")
    sql_output.append("-- =============================================")
    df = pd.read_csv('Material_type_import.csv', encoding='utf-8-sig')
    for _, row in df.iterrows():
        name = escape_sql_string(row['Тип материала'])
        waste = row['Процент потерь сырья']
        sql = f"INSERT INTO Material_types (material_type_name, waste_percentage) VALUES ({name}, {waste});"
        sql_output.append(sql)
    sql_output.append("")
    
    # 2. Product_types
    sql_output.append("-- =============================================")
    sql_output.append("-- Импорт типов продукции")
    sql_output.append("-- =============================================")
    df = pd.read_csv('Product_type_import.csv', encoding='utf-8-sig')
    for _, row in df.iterrows():
        name = escape_sql_string(row['Тип продукции'])
        coef = row['Коэффициент типа продукции']
        sql = f"INSERT INTO Product_types (product_type_name, type_coefficient) VALUES ({name}, {coef});"
        sql_output.append(sql)
    sql_output.append("")
    
    # 3. Workshops
    sql_output.append("-- =============================================")
    sql_output.append("-- Импорт цехов")
    sql_output.append("-- =============================================")
    df = pd.read_csv('Workshops_import.csv', encoding='utf-8-sig')
    for _, row in df.iterrows():
        name = escape_sql_string(row['Название цеха'])
        w_type = escape_sql_string(row['Тип цеха'])
        staff = int(row['Количество человек для производства '])
        sql = f"INSERT INTO Workshops (workshop_name, workshop_type, staff_count) VALUES ({name}, {w_type}, {staff});"
        sql_output.append(sql)
    sql_output.append("")
    
    # 4. Products
    sql_output.append("-- =============================================")
    sql_output.append("-- Импорт продукции")
    sql_output.append("-- =============================================")
    df = pd.read_csv('Products_import.csv', encoding='utf-8-sig')
    for _, row in df.iterrows():
        p_type = escape_sql_string(row['Тип продукции'])
        name = escape_sql_string(row['Наименование продукции'])
        article = int(row['Артикул'])
        price = row['Минимальная стоимость для партнера']
        material = escape_sql_string(row['Основной материал'])
        
        sql = f"""INSERT INTO Products (product_name, article_number, product_type_id, material_type_id, min_partner_price)
VALUES ({name}, '{article}', 
    (SELECT product_type_id FROM Product_types WHERE product_type_name = {p_type}),
    (SELECT material_type_id FROM Material_types WHERE material_type_name = {material}),
    {price});"""
        sql_output.append(sql)
    sql_output.append("")
    
    # 5. Product_workshops
    sql_output.append("-- =============================================")
    sql_output.append("-- Импорт связей продукции с цехами")
    sql_output.append("-- =============================================")
    df = pd.read_csv('Product_workshops_import.csv', encoding='utf-8-sig')
    for _, row in df.iterrows():
        p_name = escape_sql_string(row['Наименование продукции'])
        w_name = escape_sql_string(row['Название цеха'])
        time_h = row['Время изготовления, ч']
        
        sql = f"""INSERT INTO Product_workshops (product_id, workshop_id, production_time_hours)
VALUES (
    (SELECT product_id FROM Products WHERE product_name = {p_name}),
    (SELECT workshop_id FROM Workshops WHERE workshop_name = {w_name}),
    {time_h});"""
        sql_output.append(sql)
    
    # Сохраняем в файл
    with open('data_import.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_output))
    
    print("SQL скрипт импорта данных создан: data_import.sql")
    print(f"Всего строк: {len(sql_output)}")

if __name__ == "__main__":
    generate_inserts()
