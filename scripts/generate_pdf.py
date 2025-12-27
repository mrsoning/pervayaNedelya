import os
import sys

def generate_pdf():
    # создаем пдф из хтмл файла
    
    print("генерируем pdf...")
    print()
    
    # пути к фалам
    html_path = os.path.join('diagrams', 'ER_diagram.html')
    pdf_path = os.path.join('diagrams', 'ER_diagram.pdf')
    
    # проверяем что файл есьт
    if not os.path.exists(html_path):
        print(f"файл {html_path} не найден")
        return False
    
    print(f"из: {html_path}")
    print(f"в: {pdf_path}")
    print()
    
    # пробуем разные способы
    
    # способ 1: weasyprint
    try:
        print("пробуем weasyprint...")
        from weasyprint import HTML, CSS
        
        # читаем хтмл файл
        html = HTML(filename=html_path)
        
        # делаем пдф из него
        html.write_pdf(pdf_path)
        
        print("готово с weasyprint")
        print(f"файл: {pdf_path}")
        print()
        print("размер:", os.path.getsize(pdf_path), "байт")
        return True
        
    except ImportError:
        print("weasyprint не установлен")
        print("   pip install weasyprint")
        print()
    except Exception as e:
        print(f"ошибка weasyprint: {e}")
        print()
    
    # способ 2: pdfkit
    try:
        print("пробуем pdfkit...")
        import pdfkit
        
        options = {
            'page-size': 'A4',
            'orientation': 'Portrait',
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm',
            'encoding': 'UTF-8',
            'enable-local-file-access': None
        }
        
        pdfkit.from_file(html_path, pdf_path, options=options)
        
        print("готово с pdfkit")
        print(f"файл: {pdf_path}")
        return True
        
    except ImportError:
        print("pdfkit не установлен")
        print("   pip install pdfkit")
        print("   нужен wkhtmltopdf")
        print()
    except Exception as e:
        print(f"ошибка pdfkit: {e}")
        print()
    
    # способ 3: xhtml2pdf
    try:
        print("пробуем xhtml2pdf...")
        from xhtml2pdf import pisa
        
        with open(html_path, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
        
        with open(pdf_path, 'wb') as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        
        if not pisa_status.err:
            print("готово с xhtml2pdf")
            print(f"файл: {pdf_path}")
            return True
        else:
            print(f"ошибка xhtml2pdf: {pisa_status.err}")
            print()
            
    except ImportError:
        print("xhtml2pdf не установлен")
        print("   pip install xhtml2pdf")
        print()
    except Exception as e:
        print(f"ошибка xhtml2pdf: {e}")
        print()
    
    # ничего не получилось
    print("не удалось создать pdf")
    print()
    print("что делать:")
    print()
    print("1. установить weasyprint:")
    print("   pip install weasyprint")
    print()
    print("2. или вручную:")
    print("   - открыть diagrams/ER_diagram.html")
    print("   - ctrl+p")
    print("   - сохранить как pdf")
    print()
    
    return False

if __name__ == "__main__":
    success = generate_pdf()
    sys.exit(0 if success else 1)
