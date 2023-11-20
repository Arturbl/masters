const mongoose = require('mongoose');

const username = 'root';
const password = 'rootpassword';
const databaseName = 'admin';

const connectionString = `mongodb://${username}:${password}@localhost:27017/${databaseName}`;

mongoose.connect(connectionString, { useNewUrlParser: true, useUnifiedTopology: true });

const companySchema = new mongoose.Schema({
    company_id: { type: Number, required: true, unique: true },
    name: String,
    description: String,
    company_size: Number,
    state: String,
    country: String,
    city: String,
    zip_code: String,
    address: String,
    url: String
});

const jobPositionSchema = new mongoose.Schema({
    job_id: { type: Number, required: true, unique: true },
    company_id: { type: Number, required: true },
    title: String,
    description: String,
    max_salary: Number,
    med_salary: Number,
    min_salary: Number,
    pay_period: String,
    formatted_work_type: String,
    location: String,
    applies: Number,
    original_listed_time: Number,
    remote_allowed: Number,
    views: Number,
    job_posting_url: String,
    application_url: String,
    application_type: String,
    expiry: Date,
    closed_time: Date,
    formatted_experience_level: String,
    skills_desc: String,
    listed_time: Date,
    posting_domain: String,
    sponsored: Number,
    work_type: String,
    currency: String,
    compensation_type: String,
    scraped: Number
});

const employeeCountSchema = new mongoose.Schema({
    company_id: { type: Number, required: true, unique: true },
    employee_count: Number,
    follower_count: Number,
    time_record: Number
});

const benefitSchema = new mongoose.Schema({
    job_id: { type: Number, required: true },
    inferred: Number,
    type: String
});

const salarySchema = new mongoose.Schema({
    salary_id: { type: Number, required: true, unique: true },
    job_id: { type: Number, required: true },
    max_salary: Number,
    med_salary: Number,
    min_salary: Number,
    pay_period: String,
    currency: String,
    compensation_type: String
});

const Company = mongoose.model('Company', companySchema);
const JobPosition = mongoose.model('JobPosition', jobPositionSchema);
const EmployeeCount = mongoose.model('EmployeeCount', employeeCountSchema);
const Benefit = mongoose.model('Benefit', benefitSchema);
const Salary = mongoose.model('Salary', salarySchema);

module.exports = { Company, JobPosition, EmployeeCount, Benefit, Salary };
