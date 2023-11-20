CREATE TABLE companies (
   company_id int,
   name longtext,
   description longtext,
   company_size int,
   state longtext,
   country longtext,
   city longtext,
   zip_code longtext,
   address longtext,
   url longtext,
   PRIMARY KEY (company_id)
);

CREATE TABLE job_positions (
   job_id int,
   company_id int,
   title longtext,
   description longtext,
   max_salary float,
   med_salary float,
   min_salary float,
   pay_period longtext,
   formatted_work_type longtext,
   location longtext,
   applies int,
   original_listed_time float,
   remote_allowed int,
   views int,
   job_posting_url longtext,
   application_url longtext,
   application_type longtext,
   expiry Date,
   closed_time Date,
   formatted_experience_level longtext,
   skills_desc longtext,
   listed_time Date,
   posting_domain longtext,
   sponsored int,
   work_type longtext,
   currency longtext,
   compensation_type longtext,
   scraped long,
   PRIMARY KEY (job_id),
   FOREIGN KEY (company_id) REFERENCES Companies (company_id)
);

CREATE TABLE employee_counts (
     company_id int ,
     employee_count int,
     follower_count int,
     time_record float,
     FOREIGN KEY (company_id) REFERENCES Companies (company_id)
);

CREATE TABLE benefits (
      job_id int,
      inferred int,
      type varchar(255),
      FOREIGN KEY (job_id) REFERENCES Job_positions (job_id)
);

CREATE TABLE salaries (
  salary_id int,
  job_id int,
  max_salary float,
  med_salary float,
  min_salary float,
  pay_period varchar(255),
  currency varchar(255),
  compensation_type varchar(255),
  PRIMARY KEY (salary_id),
  FOREIGN KEY (job_id) REFERENCES Job_positions (job_id)
);
