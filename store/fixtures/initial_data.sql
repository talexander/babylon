INSERT INTO measure (name, alias, descr) VALUES 
('шт.', 'pieces', 'штука'),
('кг.', 'kg', 'килограмм'),
('гр.', 'gr', 'грамм'),
('л.', 'l', 'литр'),
('мл.', 'ml', 'миллилитр'),
('упак.', 'packet', 'упаковка');

INSERT INTO property_group (alias, name) VALUES 
('common', 'общие')
;

SET @COMMON_PROP_GROUP_ID = NULL; 
SELECT @COMMON_PROP_GROUP_ID := id FROM property_group WHERE alias='common';

INSERT INTO property (alias, name, measure, property_group) VALUES 
('pic', 'Картинка', NULL, @COMMON_PROP_GROUP_ID),
('tag', 'Тег', NULL, @COMMON_PROP_GROUP_ID)
--,()
--,()
;

INSERT INTO good_category (name, flags) VALUES
('Аюрведическая косметика', 0)
,('Книги', 0)
,('Масла', 0) 
,('Продукты для суши', 0)
,('Рис', 0)  
,('Сладости и сахар', 0) 
,('Соусы', 0)
,('СПЕЦИИ И ТРАВЫ', 0)
,('Сухофрукты', 0)
,('Чай', 0)
,('Благовония', 0)
;

TRUNCATE good_category;
INSERT INTO good_category (name, alias, flags) VALUES
('Специи', 'specii', 0),
('Травы', 'travy', 0),
('Масла', 'masla', 0),
('Мука', 'muka', 0),
('Крупа', 'krupa', 0),
('Бобовые', 'bobvie', 0),
('Консервы', 'konservy', 0),
('Продукты для суши','sushi', 0),
('Рис', 'ris', 0),
('Сахар и сладости', 'sahar-i-sladosti', 0),
('Масалы', 'masali', 0),
('Чай', 'chai', 0),
('Аюрведический чай', 'ayurvedicheskij-chaj', 0),
('Благовония', 'blagovoniya', 0),
('Ароматерапия', 'aromoterapiya', 0),
('Книги', 'knigi',0),
('Бижутерия', 'bizhuteriya',0),
('Биолокация', 'биолокация', 0),
('Игры, головоломки', 'igry-golovolomki', 0);





















