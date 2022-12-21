CREATE TABLE hitmancompany.users (
  id int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Identify the user in the hitman company',
  email varchar(255) NOT  NULL COMMENT 'THE USER''S EMAIL ADDRESS',
  name varchar(255) NOT NULL COMMENT 'THE USER''S NAME WHICH IS',
  password varchar(128) NOT NULL DEFAULT '' COMMENT 'THE USER''S ENCRYPTED PASSWORD',
  description varchar(255) NOT NULL COMMENT 'THE USER''S DESCRIPTION',
  user_status varchar(255) NOT NULL DEFAULT 'Active' COMMENT 'The current user status',
  role varchar(255) NOT  NULL DEFAULT 'Hitman' COMMENT 'THE USER''S ROLE',
  PRIMARY KEY (id),
  UNIQUE KEY name (name),
  UNIQUE KEY email (email)
) ENGINE=InnoDB;
