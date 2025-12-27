# База данных системы управления продукцией мебельной компании

## Описание проекта

Разработана база данных для системы управления продукцией мебельной компании, которая обеспечивает:
- Просмотр списка продукции
- Добавление/редактирование данных о продукции
- Просмотр списка цехов для производства продукции

## Структура базы данных

База данных находится в **3-й нормальной форме (3НФ)** с обеспечением ссылочной целостности.

### Таблицы

#### 1. Material_types (Типы материалов)
Справочник типов материалов, используемых в производстве.

**Поля:**
- `material_type_id` (INT, PK) - уникальный идентификатор
- `material_type_name` (VARCHAR(100), UNIQUE) - название материала
- `waste_percentage` (DECIMAL(5,4)) - процент потерь сырья
- `description` (TEXT) - описание
- `is_ecological` (BOOLEAN) - экологичность материала
- `created_at` (TIMESTAMP) - дата создания записи

#### 2. Product_types (Типы продукции)
Справочник типов продукции (гостиные, прихожие, мягкая мебель и т.д.).

**Поля:**
- `product_type_id` (INT, PK) - уникальный идентификатор
- `product_type_name` (VARCHAR(100), UNIQUE) - название типа
- `type_coefficient` (DECIMAL(5,2)) - коэффициент типа продукции
- `style` (VARCHAR(50)) - стиль (современный, классический)
- `description` (TEXT) - описание
- `created_at` (TIMESTAMP) - дата создания записи

#### 3. Workshops (Цеха)
Информация о производственных цехах.

**Поля:**
- `workshop_id` (INT, PK) - уникальный идентификатор
- `workshop_name` (VARCHAR(100), UNIQUE) - название цеха
- `workshop_type` (VARCHAR(100)) - тип цеха (проектирование, обработка, сборка)
- `staff_count` (INT) - количество сотрудников
- `location` (VARCHAR(200)) - расположение
- `equipment_description` (TEXT) - описание оборудования
- `is_active` (BOOLEAN) - активность цеха
- `created_at` (TIMESTAMP) - дата создания записи

#### 4. Products (Продукция)
Основная таблица с информацией о продукции.

**Поля:**
- `product_id` (INT, PK) - уникальный идентификатор
- `product_name` (VARCHAR(200)) - наименование продукции
- `article_number` (VARCHAR(50), UNIQUE) - артикул
- `product_type_id` (INT, FK) - ссылка на тип продукции
- `material_type_id` (INT, FK) - ссылка на тип материала
- `min_partner_price` (DECIMAL(10,2)) - минимальная стоимость для партнера
- `dimensions` (VARCHAR(100)) - размеры
- `weight` (DECIMAL(8,2)) - вес
- `description` (TEXT) - описание
- `is_available` (BOOLEAN) - доступность
- `created_at` (TIMESTAMP) - дата создания
- `updated_at` (TIMESTAMP) - дата обновления

**Внешние ключи:**
- `product_type_id` → `Product_types(product_type_id)`
- `material_type_id` → `Material_types(material_type_id)`

#### 5. Product_workshops (Связь продукции с цехами)
Связующая таблица между продукцией и цехами (отношение многие-ко-многим).

**Поля:**
- `product_workshop_id` (INT, PK) - уникальный идентификатор
- `product_id` (INT, FK) - ссылка на продукцию
- `workshop_id` (INT, FK) - ссылка на цех
- `production_time_hours` (DECIMAL(6,2)) - время производства в часах
- `priority` (INT) - приоритет производства
- `notes` (TEXT) - примечания
- `created_at` (TIMESTAMP) - дата создания записи

**Внешние ключи:**
- `product_id` → `Products(product_id)`
- `workshop_id` → `Workshops(workshop_id)`

**Ограничения:**
- UNIQUE(product_id, workshop_id) - уникальная пара продукт-цех

### Представления (Views)

#### v_products_full
Полная информация о продукции с названиями типов и материалов.

#### v_products_workshops
Информация о продукции с цехами производства.

### Индексы

Созданы индексы для оптимизации запросов:
- `idx_products_type` - по типу продукции
- `idx_products_material` - по типу материала
- `idx_products_available` - по доступности
- `idx_pw_product` - по продукции в связях
- `idx_pw_workshop` - по цехам в связях
- `idx_workshops_active` - по активности цехов

## ER-диаграмма

```
┌─────────────────┐         ┌──────────────────┐
│ Material_types  │         │  Product_types   │
├─────────────────┤         ├──────────────────┤
│ PK material_... │         │ PK product_ty... │
│    material_... │         │    product_ty... │
│    waste_per... │         │    type_coeff... │
└────────┬────────┘         └────────┬─────────┘
         │                           │
         │ 1                         │ 1
         │                           │
         │                           │
         │ N                         │ N
    ┌────┴──────────────────────────┴────┐
    │          Products                   │
    ├─────────────────────────────────────┤
    │ PK product_id                       │
    │    product_name                     │
    │    article_number                   │
    │ FK product_type_id                  │
    │ FK material_type_id                 │
    │    min_partner_price                │
    └────────────────┬────────────────────┘
                     │
                     │ 1
                     │
                     │ N
         ┌───────────┴──────────────┐
         │  Product_workshops       │
         ├──────────────────────────┤
         │ PK product_workshop_id   │
         │ FK product_id            │
         │ FK workshop_id           │
         │    production_time_hours │
         └───────────┬──────────────┘
                     │
                     │ N
                     │
                     │ 1
              ┌──────┴────────┐
              │   Workshops   │
              ├───────────────┤
              │ PK workshop_id│
              │    workshop...│
              │    workshop...│
              │    staff_count│
              └───────────────┘
```

## Файлы проекта

1. **full_database_script.sql** - полный скрипт создания БД с данными
2. **database_schema.sql** - только схема БД без данных
3. **data_import.sql** - только данные для импорта
4. **ER_diagram.puml** - ER-диаграмма в формате PlantUML
5. **README_DATABASE.md** - данный файл с документацией

## Установка и использование

### 1. Создание базы данных

Выполните скрипт в MySQL:

```bash
mysql -u root -p < full_database_script.sql
```

Или через MySQL Workbench:
1. Откройте файл `full_database_script.sql`
2. Выполните скрипт (Execute SQL Script)

### 2. Проверка данных

После импорта в базе данных будет:
- 4 типа материалов
- 6 типов продукции
- 12 цехов
- 20 единиц продукции
- 130 связей продукции с цехами

### 3. Примеры запросов

#### Просмотр всей продукции с полной информацией:
```sql
SELECT * FROM v_products_full;
```

#### Просмотр продукции с цехами:
```sql
SELECT * FROM v_products_workshops;
```

#### Добавление новой продукции:
```sql
INSERT INTO Products (product_name, article_number, product_type_id, material_type_id, min_partner_price)
VALUES ('Новый диван', '9999999', 
    (SELECT product_type_id FROM Product_types WHERE product_type_name = 'Мягкая мебель'),
    (SELECT material_type_id FROM Material_types WHERE material_type_name = 'Фанера'),
    45000);
```

#### Просмотр списка цехов:
```sql
SELECT * FROM Workshops WHERE is_active = TRUE;
```

#### Поиск продукции по типу:
```sql
SELECT p.*, pt.product_type_name, mt.material_type_name
FROM Products p
JOIN Product_types pt ON p.product_type_id = pt.product_type_id
JOIN Material_types mt ON p.material_type_id = mt.material_type_id
WHERE pt.product_type_name = 'Мягкая мебель';
```

#### Продукция с временем производства по цехам:
```sql
SELECT 
    p.product_name,
    w.workshop_name,
    w.workshop_type,
    pw.production_time_hours
FROM Products p
JOIN Product_workshops pw ON p.product_id = pw.product_id
JOIN Workshops w ON pw.workshop_id = w.workshop_id
ORDER BY p.product_name, pw.production_time_hours;
```

## Соответствие 3НФ

База данных соответствует третьей нормальной форме:

1. **1НФ**: Все атрибуты атомарны, нет повторяющихся групп
2. **2НФ**: Все неключевые атрибуты полностью зависят от первичного ключа
3. **3НФ**: Отсутствуют транзитивные зависимости неключевых атрибутов

## Ссылочная целостность

Обеспечена через:
- Первичные ключи (PRIMARY KEY) во всех таблицах
- Внешние ключи (FOREIGN KEY) с каскадными операциями
- Ограничения UNIQUE для уникальных полей
- Правила ON DELETE и ON UPDATE для поддержания целостности

## Генерация ER-диаграммы в PDF

Для создания PDF-версии ER-диаграммы используйте PlantUML:

1. Установите PlantUML: https://plantuml.com/ru/download
2. Выполните команду:
```bash
java -jar plantuml.jar ER_diagram.puml
```

Или используйте онлайн-редактор: https://www.plantuml.com/plantuml/

## Автор

Разработано для мебельной компании
Дата: Декабрь 2025
