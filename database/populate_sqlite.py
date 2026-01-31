#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Импорт справочных данных в SQLite (типы продукции, материалы).
Запускать при пустых выпадающих списках. Работает с открытой БД.
"""
import sqlite3
from pathlib import Path

def populate():
    db_path = Path(__file__).parent / 'furniture_company.db'
    data_dir = Path(__file__).parent.parent / 'data'
    
    if not db_path.exists():
        print("БД не найдена. Сначала запустите: python database/create_sqlite.py")
        return False
    
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        conn.execute("PRAGMA busy_timeout = 5000")
        cursor = conn.cursor()
        
        # Проверка существования таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Material_types'")
        if not cursor.fetchone():
            print("Таблицы не найдены. Остановите веб-приложение и запустите:")
            print("  python database/create_sqlite.py")
            conn.close()
            return False
        
        # Material_types
        n = cursor.execute("SELECT COUNT(*) FROM Material_types").fetchone()[0]
        if n == 0:
            import csv
            with open(data_dir / 'Material_type_import.csv', encoding='utf-8-sig') as f:
                r = csv.DictReader(f)
                for row in r:
                    cursor.execute(
                        "INSERT INTO Material_types (material_type_name, waste_percentage) VALUES (?, ?)",
                        (row['Тип материала'], row['Процент потерь сырья'])
                    )
            print("OK Material_types: imported")
        else:
            print(f"  Material_types: {n} records")
        
        # Product_types
        n = cursor.execute("SELECT COUNT(*) FROM Product_types").fetchone()[0]
        if n == 0:
            import csv
            with open(data_dir / 'Product_type_import.csv', encoding='utf-8-sig') as f:
                r = csv.DictReader(f)
                for row in r:
                    cursor.execute(
                        "INSERT INTO Product_types (product_type_name, type_coefficient) VALUES (?, ?)",
                        (row['Тип продукции'], row['Коэффициент типа продукции'])
                    )
            print("OK Product_types: imported")
        else:
            print(f"  Product_types: {n} records")
        
        conn.commit()
        conn.close()
        print("\nDone. Refresh the page in browser.")
        return True
    except sqlite3.OperationalError as e:
        if "locked" in str(e).lower() or "busy" in str(e).lower():
            print("БД занята. Остановите веб-приложение (Ctrl+C), затем запустите снова:")
            print("  python database/populate_sqlite.py")
        else:
            print(f"Ошибка: {e}")
        return False

if __name__ == "__main__":
    populate()
