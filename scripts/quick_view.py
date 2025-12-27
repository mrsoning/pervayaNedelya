from db_manager import DatabaseManager
import sys

def main():
    # быстрый просмотр базы данных
    if len(sys.argv) < 2:
        print("как использовать:")
        print("  python quick_view.py products    - продукция")
        print("  python quick_view.py workshops   - цеха")
        print("  python quick_view.py stats       - статистика")
        return
    
    command = sys.argv[1].lower()
    
    try:
        db = DatabaseManager()
        
        if command == 'products':
            products = db.get_products(limit=10)
            print(f"\nпродукция (первые 10):")
            print("-" * 50)
            
            for p in products:
                print(f"- {p['product_name']}")
                print(f"  артикул: {p['article_number']} | цена: {p['min_partner_price']:,.0f} руб")
                print(f"  тип: {p['product_type_name']} | материал: {p['material_type_name']}")
                print()
        
        elif command == 'workshops':
            workshops = db.get_workshops()
            print(f"\nцеха:")
            print("-" * 50)
            
            for w in workshops:
                status = "+" if w['is_active'] else "-"
                print(f"{status} {w['workshop_name']}")
                print(f"  тип: {w['workshop_type']} | персонал: {w['staff_count']} чел")
                print()
        
        elif command == 'stats':
            stats = db.get_statistics()
            print(f"\nстатистика бд:")
            print("-" * 50)
            
            for table, count in stats.items():
                print(f"{table}: {count} записей")
            
            print(f"\nвсего: {sum(stats.values())} записей")
        
        else:
            print(f"неизвестная команда: {command}")
    
    except Exception as e:
        print(f"ошибка: {e}")

if __name__ == "__main__":
    main()
