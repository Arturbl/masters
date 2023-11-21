CREATE TABLE companies (
   company_id bigint,
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

CREATE TABLE job_postings (
   job_id bigint,
   company_id bigint,
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
   expiry bigint, -- this is a date
   closed_time bigint, -- this is a date
   formatted_experience_level longtext,
   skills_desc longtext,
   listed_time bigint, -- this is a date
   posting_domain longtext,
   sponsored int,
   work_type longtext,
   currency longtext,
   compensation_type longtext,
   scraped long,
   PRIMARY KEY (job_id),
   FOREIGN KEY (company_id) REFERENCES companies (company_id)
);

CREATE TABLE employee_counts (
     company_id bigint ,
     employee_count int,
     follower_count int,
     time_record float,
     FOREIGN KEY (company_id) REFERENCES companies (company_id)
);

CREATE TABLE benefits (
      job_id bigint,
      inferred int,
      type varchar(255),
      FOREIGN KEY (job_id) REFERENCES job_postings (job_id)
);

CREATE TABLE salaries (
  salary_id bigint,
  job_id bigint,
  max_salary float,
  med_salary float,
  min_salary float,
  pay_period varchar(255),
  currency varchar(255),
  compensation_type varchar(255),
  PRIMARY KEY (salary_id),
  FOREIGN KEY (job_id) REFERENCES job_postings (job_id)
);
