-- Очистка таблиц
TRUNCATE TABLE 
    yield_data,
    quality_parameters,
    disease_resistances,
    patents,
    variety_regions,
    variety_authors,
    variety_applicants,
    varieties,
    applicants,
    authors,
    diseases,
    regions
RESTART IDENTITY CASCADE;

-- Регионы (латинскими символами)
INSERT INTO regions (name) VALUES
('Central Region'),
('North-West Region'),
('Southern Region'),
('Volga Region'),
('Ural Region');

-- Авторы (латинскими символами)
INSERT INTO authors (name, organization) VALUES
('Ivanov A.A.', 'Research Institute'),
('Petrova S.I.', 'Agricultural Academy'),
('Sidorov V.V.', 'Seed Institute'),
('Kuznetsova O.P.', 'Food Center');

-- Патентообладатели
INSERT INTO applicants (name, address) VALUES
('Agroholding Rostok', 'Moscow, Central st. 1'),
('Niva Farm', 'Krasnodar, Zernovaya st. 25'),
('Seed Production', 'St. Petersburg, Science av. 10');

-- Болезни
INSERT INTO diseases (name) VALUES
('Brown rust'),
('Powdery mildew'),
('Fusarium head blight');

-- Сорта растений
INSERT INTO varieties (name, type, "group", code, description, origin, registration_year) VALUES
('Krasnodarskaya 99', 'Winter wheat', 'Soft', 'KR-99', 'High-yield variety', 'Russia', 2015),
('Sibirskiy 17', 'Spring barley', 'Food', 'SB-17', 'Frost-resistant', 'Russia', 2017),
('Severny Oats', 'Spring oats', 'Feed', 'SN-01', 'High protein content', 'Russia', 2018),
('Moskovskaya Rye', 'Winter rye', 'Bakery', 'MR-2020', 'Lodging-resistant', 'Russia', 2020);

-- Теперь добавляем связи (после создания всех основных записей)
INSERT INTO variety_authors (variety_id, author_id) VALUES
(1, 1), (1, 2),
(2, 3),
(3, 4),
(4, 1), (4, 4);

INSERT INTO variety_applicants (variety_id, applicant_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 1);

INSERT INTO variety_regions (variety_id, region_id) VALUES
(1, 1), (1, 3),
(2, 1), (2, 2), (2, 4),
(3, 2), (3, 4),
(4, 1), (4, 3);

-- Данные урожайности
INSERT INTO yield_data (variety_id, region_id, average_yield, max_yield) VALUES
(1, 1, 5.2, 6.1),
(1, 3, 5.8, 6.5),
(2, 1, 4.1, 4.8),
(2, 2, 3.9, 4.5),
(3, 2, 3.8, 4.2),
(4, 1, 4.5, 5.0);