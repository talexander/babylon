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
