INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES 
  (94, 'Allowed to visit Admin Center', 15, 'view_admin_center');

INSERT INTO `auth_group_permissions` (`group_id`, `permission_id`) VALUES 
  (2, 94),
  (3, 94),
  (4, 94),
  (5, 94);


