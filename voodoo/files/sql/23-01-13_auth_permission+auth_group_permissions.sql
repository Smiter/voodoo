INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES 
  (94, 'Allowed to visit Admin Center', 15, 'view_admin_center');
COMMIT;

INSERT INTO `auth_group_permissions` (`group_id`, `permission_id`) VALUES 
  (2, 43),
  (2, 44),
  (2, 52),
  (2, 58),
  (2, 59),
  (2, 94),
  (3, 94),
  (4, 94),
  (5, 73),
  (5, 94);

COMMIT;
