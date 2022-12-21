CREATE TABLE hitmancompany.jobs (
  job_id int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID of the job',
  assigned_to int(11)unsigned NOT  NULL COMMENT 'THE USER''S RESPONSABLE FOR THE JOB',
  assigned_by int(11)unsigned NOT  NULL COMMENT 'THE USER''S WHO ASSIGNED THE JOB',
  description varchar(255) NOT NULL COMMENT 'THE USER''S DESCRIPTION',
  status_job varchar(255) NOT NULL DEFAULT 'Assigned' COMMENT 'The current job status',
  target_name varchar(255) NOT  NULL COMMENT 'THE NAME OF THE HIT JOB',
  PRIMARY KEY (job_id),
  foreign key (assigned_to) references hitmancompany.users (id),
  foreign key (assigned_by) references hitmancompany.users (id)
) ENGINE=InnoDB;