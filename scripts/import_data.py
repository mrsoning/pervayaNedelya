"""
Скрипт для импорта данных из Excel файлов в базу данных
"""
import pandas as pd
import os

def read_excel_files():
    """Читает все Excel файлы и выводит их структуру"""
    
    excel_files = [
        'Material_type_import.xlsx',
        'Product_type_import.xlsx',
        'Workshops_import.xlsx',
        'Products_import.xlsx',
        'Product_workshops_import.xlsx'
    ]
    
    for file in excel_files:
        if os.path.exists(file):
            print(f"\n{'='*60}")
            print(f"Файл: {file}")
            print('='*60)
            
            try:
                df = pd.read_excel(file)
                print(f"\nКолонки: {list(df.columns)}")
                print(f"Количество строк: {len(df)}")
                print(f"\nПервые 3 строки:")
                print(df.head(3).to_string())
                
                # Сохраняем в CSV для удобства импорта
                csv_file = file.replace('.xlsx', '.csv')
                df.to_csv(csv_file, index=False, encoding='utf-8-sig')
                print(f"\nСохранено в: {csv_file}")
                
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
        else:
            print(f"\nФайл {file} не найден")

if __name__ == "__main__":
    print("Анализ файлов импорта...")
    read_excel_files()
