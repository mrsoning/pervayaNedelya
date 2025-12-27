#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Главный скрипт управления системой БД мебельной компании
"""
import os
import sys
import subprocess
from pathlib import Path

# Цвета для консоли
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Печать заголовка"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    """Печать успеха"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Печать ошибки"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    """Печать информации"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_menu():
    """Главное меню"""
    print_header("СИСТЕМА УПРАВЛЕНИЯ БД МЕБЕЛЬНОЙ КОМПАНИИ")
    print(f"{Colors.YELLOW}1.{Colors.END} Создать базу данных")
    print(f"{Colors.YELLOW}2.{Colors.END} Просмотреть продукцию")
    print(f"{Colors.YELLOW}3.{Colors.END} Добавить продукцию")
    print(f"{Colors.YELLOW}4.{Colors.END} Просмотреть цеха")
    print(f"{Colors.YELLOW}5.{Colors.END} Статистика БД")
    print(f"{Colors.YELLOW}6.{Colors.END} Создать ER-диаграмму PDF")
    print(f"{Colors.YELLOW}7.{Colors.END} Экспорт данных")
    print(f"{Colors.YELLOW}8.{Colors.END} Тестовые запросы")
    print(f"{Colors.YELLOW}0.{Colors.END} Выход")
    print()

def create_database():
    """Создание базы данных"""
    print_header("СОЗДАНИЕ БАЗЫ ДАННЫХ")
    
    db_script = Path("database/full_database_script.sql")
    if not db_script.exists():
        print_error("Файл скрипта БД не найден!")
        return
    
    print_info("Для создания БД нужны данные подключения к MySQL")
    host = input("Хост (по умолчанию localhost): ").strip() or "localhost"
    user = input("Пользователь (по умолчанию root): ").strip() or "root"
    password = input("Пароль: ").strip()
    
    try:
        cmd = f'mysql -h {host} -u {user} -p{password} < {db_script}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("База данных успешно создана!")
            print_info("Имя БД: furniture_company")
        else:
            print_error(f"Ошибка создания БД: {result.stderr}")
    except Exception as e:
        print_error(f"Ошибка: {e}")

def view_products():
    """Просмотр продукции"""
    print_header("ПРОСМОТР ПРОДУКЦИИ")
    
    from scripts.db_manager import DatabaseManager
    
    try:
        db = DatabaseManager()
        products = db.get_products()
        
        if products:
            print(f"\n{Colors.BOLD}Найдено продукции: {len(products)}{Colors.END}\n")
            for i, p in enumerate(products, 1):
                print(f"{Colors.YELLOW}{i}.{Colors.END} {p['product_name']}")
                print(f"   Артикул: {p['article_number']}")
                print(f"   Тип: {p['product_type_name']}")
                print(f"   Материал: {p['material_type_name']}")
                print(f"   Цена: {p['min_partner_price']:,.0f} руб.")
                print()
        else:
            print_info("Продукция не найдена")
    except Exception as e:
        print_error(f"Ошибка: {e}")

def add_product():
    """Добавление продукции"""
    print_header("ДОБАВЛЕНИЕ ПРОДУКЦИИ")
    
    from scripts.db_manager import DatabaseManager
    
    try:
        db = DatabaseManager()
        
        # Получаем типы
        product_types = db.get_product_types()
        material_types = db.get_material_types()
        
        print(f"{Colors.BOLD}Типы продукции:{Colors.END}")
        for i, pt in enumerate(product_types, 1):
            print(f"{i}. {pt['product_type_name']}")
        
        print(f"\n{Colors.BOLD}Типы материалов:{Colors.END}")
        for i, mt in enumerate(material_types, 1):
            print(f"{i}. {mt['material_type_name']}")
        
        print()
        name = input("Название продукции: ").strip()
        article = input("Артикул: ").strip()
        pt_idx = int(input("Номер типа продукции: ")) - 1
        mt_idx = int(input("Номер типа материала: ")) - 1
        price = float(input("Цена: "))
        
        product_type_id = product_types[pt_idx]['product_type_id']
        material_type_id = material_types[mt_idx]['material_type_id']
        
        db.add_product(name, article, product_type_id, material_type_id, price)
        print_success("Продукция успешно добавлена!")
        
    except Exception as e:
        print_error(f"Ошибка: {e}")

def view_workshops():
    """Просмотр цехов"""
    print_header("ПРОСМОТР ЦЕХОВ")
    
    from scripts.db_manager import DatabaseManager
    
    try:
        db = DatabaseManager()
        workshops = db.get_workshops()
        
        if workshops:
            print(f"\n{Colors.BOLD}Найдено цехов: {len(workshops)}{Colors.END}\n")
            for i, w in enumerate(workshops, 1):
                status = "✓ Активен" if w['is_active'] else "✗ Неактивен"
                print(f"{Colors.YELLOW}{i}.{Colors.END} {w['workshop_name']}")
                print(f"   Тип: {w['workshop_type']}")
                print(f"   Персонал: {w['staff_count']} чел.")
                print(f"   Статус: {status}")
                print()
        else:
            print_info("Цеха не найдены")
    except Exception as e:
        print_error(f"Ошибка: {e}")

def show_statistics():
    """Статистика БД"""
    print_header("СТАТИСТИКА БАЗЫ ДАННЫХ")
    
    from scripts.db_manager import DatabaseManager
    
    try:
        db = DatabaseManager()
        stats = db.get_statistics()
        
        print(f"{Colors.BOLD}Таблицы:{Colors.END}")
        for table, count in stats.items():
            print(f"  {table}: {Colors.GREEN}{count}{Colors.END} записей")
        
        total = sum(stats.values())
        print(f"\n{Colors.BOLD}Всего записей: {Colors.GREEN}{total}{Colors.END}")
        
    except Exception as e:
        print_error(f"Ошибка: {e}")

def create_er_diagram():
    """Создание ER-диаграммы"""
    print_header("СОЗДАНИЕ ER-ДИАГРАММЫ")
    
    html_file = Path("diagrams/ER_diagram.html")
    
    if html_file.exists():
        print_info(f"Откройте файл: {html_file}")
        print_info("Нажмите Ctrl+P и сохраните как PDF")
        
        # Открываем в браузере
        try:
            if sys.platform == 'win32':
                os.startfile(html_file)
            elif sys.platform == 'darwin':
                subprocess.run(['open', html_file])
            else:
                subprocess.run(['xdg-open', html_file])
            print_success("Файл открыт в браузере")
        except Exception as e:
            print_error(f"Не удалось открыть файл: {e}")
    else:
        print_error("Файл ER-диаграммы не найден!")

def export_data():
    """Экспорт данных"""
    print_header("ЭКСПОРТ ДАННЫХ")
    
    from scripts.db_manager import DatabaseManager
    
    try:
        db = DatabaseManager()
        
        print("1. Экспорт продукции в CSV")
        print("2. Экспорт цехов в CSV")
        print("3. Экспорт всех данных")
        
        choice = input("\nВыберите вариант: ").strip()
        
        if choice == '1':
            db.export_products_to_csv()
            print_success("Продукция экспортирована в data/products_export.csv")
        elif choice == '2':
            db.export_workshops_to_csv()
            print_success("Цеха экспортированы в data/workshops_export.csv")
        elif choice == '3':
            db.export_all_to_csv()
            print_success("Все данные экспортированы в папку data/")
        
    except Exception as e:
        print_error(f"Ошибка: {e}")

def test_queries():
    """Тестовые запросы"""
    print_header("ТЕСТОВЫЕ ЗАПРОСЫ")
    
    from scripts.db_manager import DatabaseManager
    
    try:
        db = DatabaseManager()
        
        print(f"{Colors.BOLD}1. Продукция по типам:{Colors.END}")
        by_type = db.get_products_by_type()
        for row in by_type:
            print(f"  {row['product_type_name']}: {row['count']} шт.")
        
        print(f"\n{Colors.BOLD}2. Средняя цена по типам:{Colors.END}")
        avg_price = db.get_average_price_by_type()
        for row in avg_price:
            print(f"  {row['product_type_name']}: {row['avg_price']:,.0f} руб.")
        
        print(f"\n{Colors.BOLD}3. Топ-5 самых дорогих товаров:{Colors.END}")
        top_products = db.get_top_expensive_products(5)
        for i, p in enumerate(top_products, 1):
            print(f"  {i}. {p['product_name']}: {p['min_partner_price']:,.0f} руб.")
        
    except Exception as e:
        print_error(f"Ошибка: {e}")

def main():
    """Главная функция"""
    while True:
        try:
            print_menu()
            choice = input(f"{Colors.BOLD}Выберите действие: {Colors.END}").strip()
            
            if choice == '1':
                create_database()
            elif choice == '2':
                view_products()
            elif choice == '3':
                add_product()
            elif choice == '4':
                view_workshops()
            elif choice == '5':
                show_statistics()
            elif choice == '6':
                create_er_diagram()
            elif choice == '7':
                export_data()
            elif choice == '8':
                test_queries()
            elif choice == '0':
                print_success("До свидания!")
                break
            else:
                print_error("Неверный выбор!")
            
            input(f"\n{Colors.BOLD}Нажмите Enter для продолжения...{Colors.END}")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Прервано пользователем{Colors.END}")
            break
        except Exception as e:
            print_error(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
