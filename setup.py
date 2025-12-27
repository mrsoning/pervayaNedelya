# установка зависимостей
import subprocess
import sys
import os

def print_step(text):
    # печать шага
    print(f"\n{text}")
    print("-" * 40)

def install_requirements():
    """Установка зависимостей"""
    print_step("Установка зависимостей Python")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Зависимости установлены успешно!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Ошибка установки зависимостей")
        return False

def check_mysql():
    """Проверка MySQL"""
    print_step("Проверка MySQL")
    
    try:
        result = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ MySQL найден: {result.stdout.strip()}")
            return True
        else:
            print("✗ MySQL не найден")
            return False
    except FileNotFoundError:
        print("✗ MySQL не установлен или не добавлен в PATH")
        return False

def create_config():
    """Создание конфигурационного файла"""
    print_step("Создание конфигурации")
    
    config_content = """# Конфигурация подключения к БД
[database]
host = localhost
user = root
password = 
database = furniture_company
"""
    
    with open('config.ini', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("✓ Файл config.ini создан")
    print("  Отредактируйте его для настройки подключения к БД")

def main():
    """Главная функция"""
    print("\n" + "="*60)
    print("  УСТАНОВКА ПРОЕКТА: БД МЕБЕЛЬНОЙ КОМПАНИИ")
    print("="*60)
    
    # Установка зависимостей
    if not install_requirements():
        print("\n⚠ Продолжить без установки зависимостей? (y/n): ", end='')
        if input().lower() != 'y':
            return
    
    # Проверка MySQL
    check_mysql()
    
    # Создание конфига
    if not os.path.exists('config.ini'):
        create_config()
    
    print("\n" + "="*60)
    print("  ✓ УСТАНОВКА ЗАВЕРШЕНА!")
    print("="*60)
    print("\nСледующие шаги:")
    print("1. Отредактируйте config.ini (если нужно)")
    print("2. Запустите: python manage.py")
    print("3. Выберите '1' для создания базы данных")
    print("\nИли используйте быстрые команды:")
    print("  python scripts/quick_view.py products")
    print("  python scripts/quick_view.py workshops")
    print("  python scripts/quick_view.py stats")
    print()

if __name__ == "__main__":
    main()
