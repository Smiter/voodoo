DELETE FROM `admin_center_menu`;

INSERT INTO `admin_center_menu` (`id`, `name`, `title`, `enabled`) VALUES
  (1,'order_create','Создание заказа',1),
  (2,'orders_management','Наши заказы',1),
  (3,'items_management','Запчасти',1),
  (4,'shipment_create','Создание отправки',1),
  (5,'shipment_management','Отправки',1),
  (6,'orders_import','Импорт заказов',1),
  (7,'xls_import','XLS импорт',1),
  (8,'service','Автосервис',1),
  (9,'user_management','Пользователи',1),
  (10,'suppliers_list','Поставщики',1),
  (11,'discount_list','Группы скидок',1);
COMMIT;