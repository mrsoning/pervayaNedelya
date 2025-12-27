#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Менеджер для работы с базой данных
"""
import mysql.connector
from mysql.connector import Error
import csv
from pathlib import Path
import os

class DatabaseManager:
    """Класс для управления БД"""
    
    def __init__(self, host='localhost', user='root', password='', database='furniture_company'):
        """Инициализация подключения"""
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4'
        }
        self.connection = None
        self.connect()
    
    def connect(self):
        """Подключение к БД"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Ошибка подключения к БД: {e}")
            # Пробуем без указания БД
            try:
                config = self.config.copy()
                del config['database']
                self.connection = mysql.connector.connect(**config)
                return True
            except:
                raise
        return False
    
    def execute_query(self, query, params=None, fetch=True):
        """Выполнение запроса"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None if fetch else False
    
    def get_products(self, limit=None):
        """Получить список продукции"""
        query = """
            SELECT 
                p.product_id,
                p.product_name,
                p.article_number,
                pt.product_type_name,
                mt.material_type_name,
                p.min_partner_price,
                p.is_available
            FROM Products p
            JOIN Product_types pt ON p.product_type_id = pt.product_type_id
            JOIN Material_types mt ON p.material_type_id = mt.material_type_id
            ORDER BY p.product_name
        """
        if limit:
            query += f" LIMIT {limit}"
        
        return self.execute_query(query)
    
    def get_product_types(self):
        """Получить типы продукции"""
        query = "SELECT * FROM Product_types ORDER BY product_type_name"
        return self.execute_query(query)
    
    def get_material_types(self):
        """Получить типы материалов"""
        query = "SELECT * FROM Material_types ORDER BY material_type_name"
        return self.execute_query(query)
    
    def get_workshops(self):
        """Получить список цехов"""
        query = """
            SELECT 
                workshop_id,
                workshop_name,
                workshop_type,
                staff_count,
                is_active
            FROM Workshops
            ORDER BY workshop_type, workshop_name
        """
        return self.execute_query(query)
    
    def add_product(self, name, article, product_type_id, material_type_id, price):
        """Добавить продукцию"""
        query = """
            INSERT INTO Products 
            (product_name, article_number, product_type_id, material_type_id, min_partner_price)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (name, article, product_type_id, material_type_id, price), fetch=False)
    
    def update_product(self, product_id, **kwargs):
        """Обновить продукцию"""
        fields = []
        values = []
        
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        
        values.append(product_id)
        query = f"UPDATE Products SET {', '.join(fields)} WHERE product_id = %s"
        
        return self.execute_query(query, tuple(values), fetch=False)
    
    def get_statistics(self):
        """Получить статистику БД"""
        tables = ['Material_types', 'Product_types', 'Workshops', 'Products', 'Product_workshops']
        stats = {}
        
        for table in tables:
            result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            if result:
                stats[table] = result[0]['count']
        
        return stats
    
    def get_products_by_type(self):
        """Продукция по типам"""
        query = """
            SELECT 
                pt.product_type_name,
                COUNT(*) as count
            FROM Products p
            JOIN Product_types pt ON p.product_type_id = pt.product_type_id
            GROUP BY pt.product_type_name
            ORDER BY count DESC
        """
        return self.execute_query(query)
    
    def get_average_price_by_type(self):
        """Средняя цена по типам"""
        query = """
            SELECT 
                pt.product_type_name,
                AVG(p.min_partner_price) as avg_price
            FROM Products p
            JOIN Product_types pt ON p.product_type_id = pt.product_type_id
            GROUP BY pt.product_type_name
            ORDER BY avg_price DESC
        """
        return self.execute_query(query)
    
    def get_top_expensive_products(self, limit=10):
        """Топ самых дорогих товаров"""
        query = """
            SELECT 
                product_name,
                min_partner_price
            FROM Products
            ORDER BY min_partner_price DESC
            LIMIT %s
        """
        return self.execute_query(query, (limit,))
    
    def get_products_with_workshops(self):
        """Продукция с цехами"""
        query = """
            SELECT 
                p.product_name,
                w.workshop_name,
                w.workshop_type,
                pw.production_time_hours
            FROM Products p
            JOIN Product_workshops pw ON p.product_id = pw.product_id
            JOIN Workshops w ON pw.workshop_id = w.workshop_id
            ORDER BY p.product_name, pw.production_time_hours
        """
        return self.execute_query(query)
    
    def export_products_to_csv(self, filename='data/products_export.csv'):
        """Экспорт продукции в CSV"""
        products = self.get_products()
        
        if products:
            Path(filename).parent.mkdir(exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=products[0].keys())
                writer.writeheader()
                writer.writerows(products)
            
            return True
        return False
    
    def export_workshops_to_csv(self, filename='data/workshops_export.csv'):
        """Экспорт цехов в CSV"""
        workshops = self.get_workshops()
        
        if workshops:
            Path(filename).parent.mkdir(exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=workshops[0].keys())
                writer.writeheader()
                writer.writerows(workshops)
            
            return True
        return False
    
    def export_all_to_csv(self):
        """Экспорт всех данных"""
        self.export_products_to_csv()
        self.export_workshops_to_csv()
        
        # Экспорт связей
        data = self.get_products_with_workshops()
        if data:
            with open('data/products_workshops_export.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
    
    def close(self):
        """Закрыть соединение"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def __del__(self):
        """Деструктор"""
        self.close()
