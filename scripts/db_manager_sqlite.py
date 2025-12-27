#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Менеджер для работы с SQLite базой данных
"""
import sqlite3
from pathlib import Path
import csv

class DatabaseManager:
    """Класс для управления SQLite БД"""
    
    def __init__(self, db_path=None):
        """Инициализация подключения"""
        if db_path is None:
            db_path = Path(__file__).parent.parent / 'database' / 'furniture_company.db'
        
        self.db_path = db_path
        self.connection = None
        self.connect()
    
    def connect(self):
        """Подключение к БД"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Для dict-like доступа
            return True
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            return False
    
    def execute_query(self, query, params=None, fetch=True):
        """Выполнение запроса"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                rows = cursor.fetchall()
                # Конвертируем в список словарей
                return [dict(row) for row in rows]
            else:
                self.connection.commit()
                return True
        except Exception as e:
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
            VALUES (?, ?, ?, ?, ?)
        """
        return self.execute_query(query, (name, article, product_type_id, material_type_id, price), fetch=False)
    
    def update_product(self, product_id, **kwargs):
        """Обновить продукцию"""
        fields = []
        values = []
        
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            values.append(value)
        
        values.append(product_id)
        query = f"UPDATE Products SET {', '.join(fields)} WHERE product_id = ?"
        
        return self.execute_query(query, tuple(values), fetch=False)
    
    def delete_product(self, product_id):
        """Удалить продукцию"""
        query = "DELETE FROM Products WHERE product_id = ?"
        return self.execute_query(query, (product_id,), fetch=False)
    
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
            LIMIT ?
        """
        return self.execute_query(query, (limit,))
    
    def search_products(self, search_term):
        """Поиск продукции"""
        query = """
            SELECT 
                p.product_id,
                p.product_name,
                p.article_number,
                pt.product_type_name,
                mt.material_type_name,
                p.min_partner_price
            FROM Products p
            JOIN Product_types pt ON p.product_type_id = pt.product_type_id
            JOIN Material_types mt ON p.material_type_id = mt.material_type_id
            WHERE p.product_name LIKE ? OR p.article_number LIKE ?
            ORDER BY p.product_name
        """
        search = f"%{search_term}%"
        return self.execute_query(query, (search, search))
    
    def close(self):
        """Закрыть соединение"""
        if self.connection:
            self.connection.close()
    
    def __del__(self):
        """Деструктор"""
        self.close()
