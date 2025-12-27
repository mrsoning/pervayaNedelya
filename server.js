const express = require('express');
const Database = require('better-sqlite3');
const path = require('path');
const bodyParser = require('body-parser');
const expressLayouts = require('express-ejs-layouts');

const app = express();
const PORT = 3000;

const db = new Database(path.join(__dirname, 'database', 'furniture_company.db'), {
  verbose: console.log
});

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(expressLayouts);
app.set('layout', 'base');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/diagrams', express.static(path.join(__dirname, 'diagrams')));

// Routes

// Home page
app.get('/', (req, res) => {
  try {
    const stats = {
      Material_types: db.prepare('SELECT COUNT(*) as count FROM Material_types').get().count,
      Product_types: db.prepare('SELECT COUNT(*) as count FROM Product_types').get().count,
      Workshops: db.prepare('SELECT COUNT(*) as count FROM Workshops').get().count,
      Products: db.prepare('SELECT COUNT(*) as count FROM Products').get().count,
      Product_workshops: db.prepare('SELECT COUNT(*) as count FROM Product_workshops').get().count
    };
    
    res.render('index', { stats });
  } catch (error) {
    res.status(500).send('Ошибка: ' + error.message);
  }
});

// Products list
app.get('/products', (req, res) => {
  try {
    const search = req.query.search || '';
    
    let query = `
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
    `;
    
    if (search) {
      query += ` WHERE p.product_name LIKE ? OR p.article_number LIKE ?`;
      const products = db.prepare(query).all(`%${search}%`, `%${search}%`);
      res.render('products', { products, search });
    } else {
      query += ` ORDER BY p.product_name`;
      const products = db.prepare(query).all();
      res.render('products', { products, search });
    }
  } catch (error) {
    res.status(500).send('Ошибка: ' + error.message);
  }
});

// Add product form
app.get('/products/add', (req, res) => {
  try {
    const productTypes = db.prepare('SELECT * FROM Product_types ORDER BY product_type_name').all();
    const materialTypes = db.prepare('SELECT * FROM Material_types ORDER BY material_type_name').all();
    
    res.render('add_product', { productTypes, materialTypes });
  } catch (error) {
    res.status(500).send('Ошибка: ' + error.message);
  }
});

// Create product
app.post('/products/add', (req, res) => {
  try {
    const { name, article, product_type_id, material_type_id, price } = req.body;
    
    const stmt = db.prepare(`
      INSERT INTO Products (product_name, article_number, product_type_id, material_type_id, min_partner_price)
      VALUES (?, ?, ?, ?, ?)
    `);
    
    stmt.run(name, article, product_type_id, material_type_id, price);
    res.redirect('/products');
  } catch (error) {
    res.status(500).send('Ошибка: ' + error.message);
  }
});

// Edit product form
app.get('/products/edit/:id', (req, res) => {
  try {
    const product = db.prepare('SELECT * FROM Products WHERE product_id = ?').get(req.params.id);
    const productTypes = db.prepare('SELECT * FROM Product_types ORDER BY product_type_name').all();
    const materialTypes = db.prepare('SELECT * FROM Material_types ORDER BY material_type_name').all();
    
    res.render('edit_product', { product, productTypes, materialTypes });
  } catch (error) {
    res.status(500).send('Ошибка: ' + error.message);
  }
});

// Update product
app.post('/products/edit/:id', (req, res) => {
  try {
    const { name, price, is_available } = req.body;
    
    const stmt = db.prepare(`
      UPDATE Products 
      SET product_name = ?, min_partner_price = ?, is_available = ?
      WHERE product_id = ?
    `);
    
    stmt.run(name, price, is_available ? 1 : 0, req.params.id);
    res.redirect('/products');
  } catch (error) {
    res.status(500).send('Ошибка: ' + error.message);
  }
});

// Delete product
app.get('/products/delete/:id', (req, res) => {
  try {
    const stmt = db.prepare('DELETE FROM Products WHERE product_id = ?');
    stmt.run(req.params.id);
    res.redirect('/products');
  } catch (error) {
    res.status(500).send('Ошибка: ' + error.message);
  }
});

// Workshops list
app.get('/workshops', (req, res) => {
  try {
    const workshops = db.prepare(`
      SELECT 
        workshop_id,
        workshop_name,
        workshop_type,
        staff_count,
        is_active
      FROM Workshops
      ORDER BY workshop_type, workshop_name
    `).all();
    
    res.render('workshops', { workshops });
  } catch (error) {
    res.status(500).send('Ошибка: ' + error.message);
  }
});

// Analytics
app.get('/analytics', (req, res) => {
  try {
    const byType = db.prepare(`
      SELECT 
        pt.product_type_name,
        COUNT(*) as count
      FROM Products p
      JOIN Product_types pt ON p.product_type_id = pt.product_type_id
      GROUP BY pt.product_type_name
      ORDER BY count DESC
    `).all();
    
    const avgPrice = db.prepare(`
      SELECT 
        pt.product_type_name,
        AVG(p.min_partner_price) as avg_price
      FROM Products p
      JOIN Product_types pt ON p.product_type_id = pt.product_type_id
      GROUP BY pt.product_type_name
      ORDER BY avg_price DESC
    `).all();
    
    const topProducts = db.prepare(`
      SELECT 
        product_name,
        min_partner_price
      FROM Products
      ORDER BY min_partner_price DESC
      LIMIT 10
    `).all();
    
    res.render('analytics', { byType, avgPrice, topProducts });
  } catch (error) {
    res.status(500).send('Ошибка: ' + error.message);
  }
});

// Report page for PDF printing
app.get('/report-pdf', (req, res) => {
  try {
    const stats = {
      Material_types: db.prepare('SELECT COUNT(*) as count FROM Material_types').get().count,
      Product_types: db.prepare('SELECT COUNT(*) as count FROM Product_types').get().count,
      Workshops: db.prepare('SELECT COUNT(*) as count FROM Workshops').get().count,
      Products: db.prepare('SELECT COUNT(*) as count FROM Products').get().count,
      Product_workshops: db.prepare('SELECT COUNT(*) as count FROM Product_workshops').get().count
    };
    
    res.render('report_pdf', { stats, layout: false });
  } catch (error) {
    res.status(500).send('Error: ' + error.message);
  }
});

// API: Statistics
app.get('/api/stats', (req, res) => {
  try {
    const stats = {
      Material_types: db.prepare('SELECT COUNT(*) as count FROM Material_types').get().count,
      Product_types: db.prepare('SELECT COUNT(*) as count FROM Product_types').get().count,
      Workshops: db.prepare('SELECT COUNT(*) as count FROM Workshops').get().count,
      Products: db.prepare('SELECT COUNT(*) as count FROM Products').get().count,
      Product_workshops: db.prepare('SELECT COUNT(*) as count FROM Product_workshops').get().count
    };
    
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// API: Products
app.get('/api/products', (req, res) => {
  try {
    const products = db.prepare(`
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
    `).all();
    
    res.json(products);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// API: Production time calculation
app.get('/api/products/:id/production-time', (req, res) => {
  try {
    const productId = req.params.id;
    
    // Получаем время производства в каждом цехе
    const workshops = db.prepare(`
      SELECT 
        w.workshop_name,
        pw.production_time_hours
      FROM Product_workshops pw
      JOIN Workshops w ON pw.workshop_id = w.workshop_id
      WHERE pw.product_id = ?
    `).all(productId);
    
    // Рассчитываем общее время
    const totalTime = workshops.reduce((sum, w) => sum + w.production_time_hours, 0);
    
    res.json({
      product_id: productId,
      workshops: workshops,
      total_production_time: Math.ceil(totalTime)
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// API: Material calculation
app.post('/api/calculate-material', (req, res) => {
  try {
    const { product_type_id, material_type_id, quantity, param1, param2 } = req.body;
    
    // Валидация входных данных
    if (!product_type_id || !material_type_id || !quantity || !param1 || !param2) {
      return res.status(400).json({ error: 'Недостаточно параметров' });
    }
    
    if (quantity <= 0 || param1 <= 0 || param2 <= 0) {
      return res.status(400).json({ error: 'Параметры должны быть положительными' });
    }
    
    // Получаем коэффициент типа продукции
    const productType = db.prepare('SELECT type_coefficient FROM Product_types WHERE product_type_id = ?').get(product_type_id);
    if (!productType) {
      return res.json({ material_needed: -1, error: 'Тип продукции не найден' });
    }
    
    // Получаем процент потерь материала
    const materialType = db.prepare('SELECT waste_percentage FROM Material_types WHERE material_type_id = ?').get(material_type_id);
    if (!materialType) {
      return res.json({ material_needed: -1, error: 'Тип материала не найден' });
    }
    
    // Расчет количества сырья на одну единицу
    const materialPerUnit = param1 * param2 * productType.type_coefficient;
    
    // Учитываем потери материала
    const materialWithWaste = materialPerUnit * (1 + materialType.waste_percentage);
    
    // Общее количество для заданного количества продукции
    const totalMaterial = Math.ceil(materialWithWaste * quantity);
    
    res.json({
      product_type_id,
      material_type_id,
      quantity,
      param1,
      param2,
      type_coefficient: productType.type_coefficient,
      waste_percentage: materialType.waste_percentage,
      material_per_unit: materialPerUnit.toFixed(2),
      material_with_waste: materialWithWaste.toFixed(2),
      material_needed: totalMaterial
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// API: Product workshops
app.get('/api/products/:id/workshops', (req, res) => {
  try {
    const productId = req.params.id;
    
    const workshops = db.prepare(`
      SELECT 
        w.workshop_id,
        w.workshop_name,
        w.workshop_type,
        w.staff_count,
        pw.production_time_hours
      FROM Product_workshops pw
      JOIN Workshops w ON pw.workshop_id = w.workshop_id
      WHERE pw.product_id = ?
      ORDER BY pw.production_time_hours DESC
    `).all(productId);
    
    res.json(workshops);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Generate ER-diagram PDF
app.get('/generate-pdf', (req, res) => {
  const { exec } = require('child_process');
  const fs = require('fs');
  const path = require('path');
  
  const pdfPath = path.join(__dirname, 'diagrams', 'ER_diagram.pdf');
  const scriptPath = path.join(__dirname, 'scripts', 'generate_pdf.py');
  
  console.log('Запуск генерации PDF...');
  
  // Запускаем Python скрипт
  exec(`python "${scriptPath}"`, (error, stdout, stderr) => {
    console.log('Вывод скрипта:', stdout);
    
    if (stderr) {
      console.error('stderr:', stderr);
    }
    
    // Проверяем существование PDF (даже если была ошибка, файл мог создаться)
    if (fs.existsSync(pdfPath)) {
      console.log('PDF файл найден, отправляем...');
      
      // Отправляем HTML страницу с автоматической загрузкой
      res.send(`
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>PDF создан</title>
          <style>
            body {
              font-family: 'Segoe UI', Arial, sans-serif;
              max-width: 800px;
              margin: 50px auto;
              padding: 40px;
              background: #f5f5f5;
            }
            .container {
              background: white;
              padding: 40px;
              border-radius: 10px;
              box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
              color: #27ae60;
              margin-bottom: 20px;
            }
            .success-icon {
              font-size: 64px;
              text-align: center;
              margin-bottom: 20px;
            }
            .btn {
              display: inline-block;
              padding: 12px 24px;
              background: #3498db;
              color: white;
              text-decoration: none;
              border-radius: 4px;
              margin-right: 10px;
              margin-top: 10px;
            }
            .btn:hover {
              background: #2980b9;
            }
            .btn-success {
              background: #27ae60;
            }
            .btn-success:hover {
              background: #229954;
            }
            .info {
              background: #e3f2fd;
              padding: 15px;
              border-radius: 4px;
              margin-top: 20px;
              border-left: 4px solid #2196f3;
            }
          </style>
          <script>
            // Автоматически начинаем загрузку PDF
            window.onload = function() {
              setTimeout(function() {
                window.location.href = '/download-pdf';
              }, 1000);
            };
          </script>
        </head>
        <body>
          <div class="container">
            <div class="success-icon">✅</div>
            <h1>PDF успешно создан!</h1>
            <p>Файл <code>diagrams/ER_diagram.pdf</code> был успешно сгенерирован.</p>
            <p>Загрузка начнется автоматически через секунду...</p>
            
            <div style="margin-top: 30px;">
              <a href="/download-pdf" class="btn btn-success">Скачать PDF</a>
              <a href="/" class="btn">Вернуться на главную</a>
              <a href="/diagrams/ER_diagram.html" target="_blank" class="btn">Открыть HTML версию</a>
            </div>
            
            <div class="info">
              <strong>Информация:</strong><br>
              PDF файл сохранен в папке <code>diagrams/</code> вашего проекта.
            </div>
          </div>
        </body>
        </html>
      `);
    } else {
      // PDF не создан
      console.error('PDF файл не найден');
      
      res.status(500).send(`
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Ошибка генерации PDF</title>
          <style>
            body {
              font-family: 'Segoe UI', Arial, sans-serif;
              max-width: 800px;
              margin: 50px auto;
              padding: 40px;
              background: #f5f5f5;
            }
            .container {
              background: white;
              padding: 40px;
              border-radius: 10px;
              box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
              color: #e74c3c;
              margin-bottom: 20px;
            }
            .error-icon {
              font-size: 64px;
              text-align: center;
              margin-bottom: 20px;
            }
            .btn {
              display: inline-block;
              padding: 12px 24px;
              background: #3498db;
              color: white;
              text-decoration: none;
              border-radius: 4px;
              margin-right: 10px;
              margin-top: 10px;
            }
            .btn:hover {
              background: #2980b9;
            }
            .warning {
              background: #fff3e0;
              padding: 15px;
              border-radius: 4px;
              margin-top: 20px;
              border-left: 4px solid #ff9800;
            }
            code {
              background: #f5f5f5;
              padding: 2px 6px;
              border-radius: 3px;
              font-family: 'Courier New', monospace;
            }
            ol {
              line-height: 1.8;
            }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="error-icon">⚠️</div>
            <h1>Не удалось создать PDF</h1>
            <p>Для автоматической генерации PDF требуется установка библиотеки <code>weasyprint</code>.</p>
            
            <div class="warning">
              <strong>Установка:</strong><br>
              <code>pip install weasyprint</code>
            </div>
            
            <h3 style="margin-top: 30px;">Альтернативный способ (ручной):</h3>
            <ol>
              <li>Откройте файл <code>diagrams/ER_diagram.html</code> в браузере</li>
              <li>Нажмите <code>Ctrl+P</code> (или <code>Cmd+P</code> на Mac)</li>
              <li>Выберите "Сохранить как PDF"</li>
              <li>Сохраните как <code>diagrams/ER_diagram.pdf</code></li>
            </ol>
            
            <div style="margin-top: 30px;">
              <a href="/" class="btn">Вернуться на главную</a>
              <a href="/diagrams/ER_diagram.html" target="_blank" class="btn">Открыть HTML версию</a>
            </div>
            
            <div class="warning" style="margin-top: 20px;">
              <strong>Вывод скрипта:</strong><br>
              <pre style="margin-top: 10px; overflow-x: auto;">${stdout || 'Нет вывода'}</pre>
            </div>
          </div>
        </body>
        </html>
      `);
    }
  });
});

// Download PDF file
app.get('/download-pdf', (req, res) => {
  const pdfPath = path.join(__dirname, 'diagrams', 'ER_diagram.pdf');
  
  if (fs.existsSync(pdfPath)) {
    res.download(pdfPath, 'ER_diagram.pdf', (err) => {
      if (err) {
        console.error('Ошибка при скачивании:', err);
        res.status(500).send('Ошибка при скачивании файла');
      }
    });
  } else {
    res.status(404).send('PDF файл не найден');
  }
});

// Start server

app.listen(PORT, () => {
  console.log('\n' + '='.repeat(60));
  console.log('  ВЕБ-ПРИЛОЖЕНИЕ: БД МЕБЕЛЬНОЙ КОМПАНИИ (Node.js)');
  console.log('='.repeat(60));
  console.log(`\n  Откройте в браузере: http://localhost:${PORT}`);
  console.log('\n  Нажмите Ctrl+C для остановки\n');
});

// Graceful shutdown
process.on('SIGINT', () => {
  db.close();
  console.log('\n\nСервер остановлен');
  process.exit(0);
});
