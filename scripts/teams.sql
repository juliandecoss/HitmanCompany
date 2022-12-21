CREATE TABLE hitmancompany.teams(
  relation_id int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID of the job',
  hitman_id int(11)unsigned NOT  NULL COMMENT 'THE USER''S RESPONSABLE FOR THE JOB',
  manager_id int(11)unsigned NOT  NULL COMMENT 'THE USER''S WHO ASSIGNED THE JOB',
  PRIMARY KEY (relation_id),
  foreign key (hitman_id) references hitmancompany.users (id),
  foreign key (manager_id) references hitmancompany.users (id)
) ENGINE=InnoDB;