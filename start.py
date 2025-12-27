# запуск системы
import subprocess
import sys
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("  ЗАПУСК СИСТЕМЫ БД МЕБЕЛЬНОЙ КОМПАНИИ")
    print("="*60 + "\n")
    
    # Проверка БД
    db_path = Path('database/furniture_company.db')
    
    if not db_path.exists():
        print("⚠️  База данных не найдена. Создаем...")
        try:
            subprocess.run([sys.executable, 'database/create_sqlite.py'], check=True)
            print("✓ База данных создана!\n")
        except Exception as e:
            print(f"✗ Ошибка создания БД: {e}")
            return
    else:
        print(f"✓ База данных найдена: {db_path}\n")
    
    # Запуск веб-приложения
    print("Выберите режим:")
    print("1. Веб-интерфейс (рекомендуется)")
    print("2. Консольное меню")
    print("0. Выход")
    
    choice = input("\nВаш выбор: ").strip()
    
    if choice == '1':
        print("\n🚀 Запуск веб-приложения...")
        print("   Откройте в браузере: http://127.0.0.1:5000")
        print("   Нажмите Ctrl+C для остановки\n")
        subprocess.run([sys.executable, 'web_app.py'])
    elif choice == '2':
        subprocess.run([sys.executable, 'manage.py'])
    else:
        print("До свидания!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма остановлена пользователем")
