# Apache Airflow ETL Pipeline Sprint Project
## Project Requirements

**Course Module**: Data Engineering Practicum  
**Project Type**: Team Sprint (3 members)  

---

## 1. Executive Summary

### 1.1 Project Title
**Rapid ETL Pipeline Development with Apache Airflow**

### 1.2 Overview
Your team will build a functional ETL pipeline that processes customer, product, and order data from CSV, JSON, and YAML files into a PostgreSQL database using Apache Airflow. This intensive sprint simulates a real-world proof-of-concept (POC) project.

### 1.3 Sprint Goals
- Deliver a working ETL pipeline within tight deadlines
- Demonstrate proficiency with Apache Airflow basics
- Show ability to handle multiple data formats
- Practice agile development in a team setting

---

## 2. Core Requirements (Minimum Viable Product)

### 2.1 Data Generation Requirements

#### 2.1.1 Data Volume (Simplified)
- Generate **exactly 1000 records** for each entity type
- **3 entity types**: Customers, Products, Orders
- **3 file formats**: CSV, JSON, YAML
- **Total**: 9 files (3 entities × 3 formats)

#### 2.1.2 Simplified Data Schema

**Customer Entity (Minimum 8 fields)**:
```
- customer_id (integer, unique)
- first_name (string)
- last_name (string)
- email (string, unique)
- phone (string)
- city (string)
- registration_date (date)
- customer_type (string: Regular/Premium/VIP)
```

**Product Entity (Minimum 7 fields)**:
```
- product_id (integer, unique)
- product_name (string)
- category (string)
- brand (string)
- unit_price (decimal)
- stock_quantity (integer)
- is_active (boolean)
```

**Order Entity (Minimum 8 fields)**:
```
- order_id (integer, unique)
- customer_id (integer, foreign key)
- order_date (timestamp)
- order_status (string: Pending/Shipped/Delivered)
- payment_method (string)
- total_amount (decimal)
- discount_amount (decimal)
- shipping_cost (decimal)
```

#### 2.1.3 Faker Implementation
- Use Python Faker library
- Create one script to generate all data
- Ensure referential integrity (orders reference valid customers)
- No need for complex data anomalies

### 2.2 Apache Airflow Requirements (Simplified)

#### 2.2.1 Single DAG Requirements
Create **ONE main DAG** with the following tasks:

1. **File Validation Task**
   - Check if all 9 files exist
   - Verify file formats are readable

2. **Database Setup Task**
   - Create tables if not exists
   - Clear staging tables

3. **Data Extraction Tasks** (Can be parallel)
   - Task for CSV files processing
   - Task for JSON files processing  
   - Task for YAML files processing

4. **Data Loading Tasks**
   - Load customers to database
   - Load products to database
   - Load orders to database (depends on customers)

5. **Data Validation Task**
   - Basic row count verification
   - Check foreign key relationships

6. **Completion Task**
   - Log pipeline success
   - Archive processed files

#### 2.2.2 Scheduling
- Set to run daily at a specific time
- Support manual triggering
- No complex scheduling patterns required

### 2.3 Database Requirements (Simplified)

#### 2.3.1 PostgreSQL Setup
- Use any PostgreSQL version 12+
- Single database with public schema
- Basic table structure (no partitioning required)

#### 2.3.2 Required Tables
```sql
-- Main tables only (no complex staging)
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(50),
    registration_date DATE,
    customer_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10,2),
    stock_quantity INTEGER,
    is_active BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMP,
    order_status VARCHAR(20),
    payment_method VARCHAR(30),
    total_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Simple audit table
CREATE TABLE etl_audit (
    run_id SERIAL PRIMARY KEY,
    dag_name VARCHAR(100),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20),
    records_processed INTEGER
);
```

### 2.4 Error Handling Requirements (Basic)
- Try-catch blocks for file operations
- Basic database error handling
- Log errors to console/file
- Email notification on failure (optional)

---

## 3. Team Structure & Responsibilities

### 3.1 Streamlined Team Roles

**Student A - Database & Backend **
- Set up PostgreSQL database
- Create all tables and schemas
- Write data loading functions
- Test database operations

**Student B - Airflow Pipeline **
- Install and configure Airflow
- Develop the main DAG
- Implement task dependencies
- Handle scheduling

**Student C - Data Generation & Testing **
- Create Faker data generation script
- Generate all 9 data files
- Write basic tests
- Prepare documentation

### 3.2 Collaboration Requirements
- Daily 15-minute stand-up meetings
- Use Git with simple branching (main + feature branches)
- Share code through GitHub/GitLab
- Use Slack/Discord for communication

---

## 4. Condensed Timeline

### Setup & Development 

**Day 1 (Monday)**
- Team kickoff meeting (1 hour)
- Environment setup
- Role assignments
- Create Git repository

**Day 2 (Tuesday)**
- Student A: Install PostgreSQL, design schema
- Student B: Install Apache Airflow locally
- Student C: Write Faker data generation script

**Day 3 (Wednesday)**
- Student A: Create database tables
- Student B: Create basic DAG structure
- Student C: Generate all data files

**Day 4 (Thursday)**
- Student A: Write data loading functions
- Student B: Implement extraction tasks
- Student C: Create basic validation scripts

**Day 5 (Friday)**
- Integration of components
- First end-to-end test
- Fix critical issues

### Week 2: Integration & Testing (Days 6-10)

**Day 6 (Monday)**
- Complete pipeline integration
- Run full pipeline tests
- Document issues found

**Day 7 (Tuesday)**
- Fix integration issues
- Add error handling
- Implement logging

**Day 8 (Wednesday)**
- Add data validation tasks
- Test with different data scenarios
- Performance testing

**Day 9 (Thursday)**
- Code cleanup and optimization
- Add comments and docstrings
- Update README file

**Day 10 (Friday)**
- Final testing
- Bug fixes
- Prepare for documentation

### Week 3: Documentation & Presentation (Days 11-15)

**Day 11 (Monday)**
- Write technical documentation
- Create architecture diagrams
- Document setup instructions

**Day 12 (Tuesday)**
- Complete user guide
- Record demo video
- Prepare presentation slides

**Day 13 (Wednesday)**
- Final code review
- Last bug fixes
- Submission preparation

**Day 14 (Thursday)**
- Final submission
- Upload to repository
- Submit documentation

**Day 15 (Friday)**
- Team presentations (10 minutes each)
- Live demos
- Q&A sessions

---

## 5. Simplified Deliverables

### 5.1 Code Deliverables
1. **Data Generation Script** (`generate_data.py`)
   - Single Python file using Faker
   - Generates all 9 files

2. **Airflow DAG** (`etl_pipeline.py`)
   - One main DAG file
   - Clear task structure

3. **Database Scripts** (`schema.sql`)
   - Table creation statements
   - Sample queries

4. **Configuration Files**
   - `requirements.txt`
   - `airflow.cfg` (if modified)
   - `.env` file for credentials

### 5.2 Documentation (Simplified)

1. **README.md** (2-3 pages)
   - Project overview
   - Setup instructions
   - How to run the pipeline
   - Team members

2. **Technical Documentation** (5-7 pages)
   - Architecture diagram
   - Database schema diagram
   - Data flow explanation
   - Key design decisions

3. **User Guide** (3-4 pages)
   - Installation steps
   - Running the pipeline
   - Troubleshooting common issues

### 5.3 Presentation Requirements
- **10-minute presentation**
- **5-minute live demo**
- **5-minute Q&A**
- All team members must participate

---

## 6. Technical Constraints

### 6.1 Required Technologies
- **Python**: 3.8+
- **Apache Airflow**: 2.0+ (pip install apache-airflow)
- **PostgreSQL**: 12+
- **Faker**: Latest version
- **Pandas**: For data processing
- **Git**: Version control

### 7.2 Development Environment
- Can use local machines or cloud IDEs
- Docker is recommended
- Windows/Mac/Linux all supported

### 7.3 Simplifications Allowed
- Can use Airflow's built-in operators only
- Can hardcode configuration for demo purposes
- Can use pandas for all file processing

---

## 8. Resources & Support

### 8.1 Quick Start Resources
- [Apache Airflow Quick Start](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
- [Faker Documentation](https://faker.readthedocs.io/)
- [PostgreSQL in 10 minutes](https://www.postgresql.org/docs/current/tutorial.html)
- Instructor-provided template DAG

### 8.2 Support Schedule
- **Daily office hours**: 4-5 PM
- **Slack/Teams channel**: 24/7 questions
- **Emergency hotline**: For blocking issues

### 8.3 Common Issues FAQ
1. **Airflow won't start**: Check Python version, try `airflow db init`
2. **Database connection fails**: Verify PostgreSQL is running, check credentials
3. **Import errors**: Ensure all packages in requirements.txt are installed
4. **DAG not visible**: Check for syntax errors, refresh Airflow UI

---

## 9. Submission Guidelines

### 9.1 What to Submit
1. **GitHub Repository** containing:
   - All code files
   - Generated data files (in `data/` folder)
   - Documentation (in `docs/` folder)
   - README.md in root

2. **Video Recording** (5-10 minutes):
   - Show pipeline running end-to-end
   - Brief explanation of architecture
   - Backup for live demo


## 10. Minimum Acceptance Criteria

### Must-Have Features 
✅ Faker script generates 1000 records per entity  
✅ All 9 files are created (3 entities × 3 formats)  
✅ Airflow DAG runs without errors  
✅ Data is loaded into PostgreSQL  
✅ Foreign key relationships are maintained  
✅ Basic documentation exists  
✅ Code is in Git repository  

### Should-Have Features 
✅ All Must-Haves plus:  
✅ Error handling implemented  
✅ Logging added to pipeline  
✅ Data validation checks  
✅ Clear documentation  
✅ Successful live demo  

### Nice-to-Have Features 
✅ All Should-Haves plus:  
✅ Automated testing  
✅ Docker containerization  
✅ Performance optimization  
✅ Monitoring dashboard  
✅ Professional presentation  

---

## Quick Start Checklist

### Day 1 Checklist
- [ ] Form team and exchange contacts
- [ ] Create shared Git repository
- [ ] Install Python 3.8+
- [ ] Set up virtual environment
- [ ] Assign primary roles

### Week 1 Goals
- [ ] Generate all data files
- [ ] Basic DAG running in Airflow
- [ ] Database tables created
- [ ] First successful data load

### Week 2 Goals
- [ ] Complete pipeline working end-to-end
- [ ] Error handling added
- [ ] Testing completed
- [ ] Code cleaned up

### Week 3 Goals
- [ ] Documentation complete
- [ ] Presentation ready
- [ ] Demo recorded
- [ ] Project submitted

---


**Important Notes:**
- Focus on getting a working solution first, optimize later
- Ask for help early if blocked
- Daily commits to Git are mandatory
- Have fun and learn by doing!

