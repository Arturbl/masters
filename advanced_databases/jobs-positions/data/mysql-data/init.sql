CREATE TABLE companies (
   company_id int,
   name varchar(255),
   description varchar(255),
   company_size int,
   state varchar(255),
   country varchar(255),
   city varchar(255),
   zip_code varchar(255),
   address varchar(255),
   url varchar(255),
   PRIMARY KEY (company_id)
);

CREATE TABLE job_positions (
   job_id int,
   company_id int,
   title varchar(255),
   description varchar(255),
   max_salary float,
   med_salary float,
   min_salary float,
   pay_period varchar(255),
   formatted_work_type varchar(255),
   location varchar(255),
   applies int,
   original_listed_time float,
   remote_allowed int,
   views int,
   job_posting_url varchar(255),
   application_url varchar(255),
   application_type varchar(255),
   expiry Date,
   closed_time Date,
   formatted_experience_level varchar(255),
   skills_desc varchar(255),
   listed_time Date,
   posting_domain varchar(255),
   sponsored int,
   work_type varchar(255),
   currency varchar(255),
   compensation_type varchar(255),
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
