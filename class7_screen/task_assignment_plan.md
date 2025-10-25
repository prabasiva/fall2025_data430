# Project Task Assignment Plan
## Web Scraping and PySpark Data Pipeline Project

**Duration:** 2 Weeks (14 Days)
**Team:** Student A, Student B, Student C

---

## Team Member Roles

### Student A: Web Scraping & Data Extraction Lead
- Primary responsibility: Web scraping module
- Secondary: Integration support

### Student B: Data Processing & PySpark Lead
- Primary responsibility: PySpark data processing
- Secondary: Data validation and quality

### Student C: Database & Infrastructure Lead
- Primary responsibility: Database design and storage
- Secondary: Project setup and documentation

---

## Week 1: Foundation & Core Development

### Days 1-2 (Setup & Planning)

#### Student A Tasks:
- [ ] Set up development environment (Python 3.8+, virtual environment)
- [ ] Install BeautifulSoup4, Requests libraries
- [ ] Analyze HTML structure of http://quotes.toscrape.com/
- [ ] Create basic scraper for single page (proof of concept)
- [ ] Document HTML structure and parsing strategy
- **Deliverable:** Working single-page scraper + documentation

#### Student B Tasks:
- [ ] Set up PySpark environment (Python + Java)
- [ ] Test basic PySpark functionality and DataFrame operations
- [ ] Design data schemas for quotes, authors, and tags
- [ ] Create sample test data for development
- [ ] Research data cleaning strategies
- **Deliverable:** PySpark environment setup + schema definitions

#### Student C Tasks:
- [ ] Choose database system (PostgreSQL recommended)
- [ ] Set up database server locally
- [ ] Design normalized database schema (ERD diagram)
- [ ] Create SQL DDL scripts for table creation
- [ ] Set up project structure (directories: src, data, logs, config, tests, docs)
- **Deliverable:** Database schema + project structure

---

### Days 3-4 (Core Module Development - Part 1)

#### Student A Tasks:
- [ ] Implement pagination logic to handle multiple pages
- [ ] Add error handling and retry logic for network failures
- [ ] Implement rate limiting (1-2 second delays)
- [ ] Add User-Agent headers to requests
- [ ] Create data extraction functions (quote text, author, tags)
- [ ] Save scraped data to JSON intermediate format
- **Deliverable:** Multi-page scraper with error handling

#### Student B Tasks:
- [ ] Create PySpark module to load JSON data
- [ ] Implement data cleaning functions:
  - Remove duplicates
  - Handle null/empty values
  - Trim whitespace
  - Validate data types
- [ ] Add data transformation logic for quote length and word count
- [ ] Test with sample data from Student A
- **Deliverable:** Data cleaning module

#### Student C Tasks:
- [ ] Implement database connection module
- [ ] Create functions for:
  - Inserting authors (with duplicate checking)
  - Inserting tags (with duplicate checking)
  - Inserting quotes
  - Managing quote-tag relationships
- [ ] Add transaction management
- [ ] Create sample database queries for testing
- **Deliverable:** Database insertion module

---

### Days 5-7 (Core Module Development - Part 2 & Integration)

#### Student A Tasks:
- [ ] Complete full website scraping (all pages)
- [ ] Add comprehensive logging (timestamps, page numbers)
- [ ] Implement metadata tracking (scrape timestamp, page number)
- [ ] Test scraper end-to-end with all pages
- [ ] Create configuration file for scraper settings
- [ ] Handle edge cases (missing tags, special characters)
- **Deliverable:** Production-ready scraper + sample scraped data

#### Student B Tasks:
- [ ] Implement data transformation for database schema
- [ ] Handle many-to-many relationship (quotes-tags)
- [ ] Create separate DataFrames for authors, quotes, tags, quote_tags
- [ ] Add data validation and quality checks
- [ ] Implement PySpark-to-database connector
- [ ] Test with full dataset from Student A
- **Deliverable:** Complete PySpark processing pipeline

#### Student C Tasks:
- [ ] Optimize database schema (indexes, constraints)
- [ ] Add foreign key relationships
- [ ] Implement upsert logic (handle re-running pipeline)
- [ ] Create database validation queries
- [ ] Set up logging for database operations
- [ ] Test database insertion with processed data from Student B
- **Deliverable:** Optimized database with insertion logic

---

## Week 2: Integration, Testing & Documentation

### Days 8-9 (Integration & End-to-End Testing)

#### All Students (Collaborative):
- [ ] **Student A:** Integrate scraper with Student B's processing module
- [ ] **Student B:** Integrate processing with Student C's database module
- [ ] **Student C:** Create main pipeline script that orchestrates all components
- [ ] Test complete pipeline end-to-end
- [ ] Fix integration bugs and issues
- [ ] Verify data consistency across all stages
- [ ] Test pipeline with multiple runs (check duplicate handling)
- **Deliverable:** Working end-to-end pipeline

---

### Days 10-11 (Testing & Quality Assurance)

#### Student A Tasks:
- [ ] Write unit tests for scraping functions
- [ ] Test pagination edge cases
- [ ] Test network error scenarios
- [ ] Validate all quotes are extracted correctly
- [ ] Create test documentation
- **Deliverable:** Scraper tests + validation report

#### Student B Tasks:
- [ ] Write unit tests for data processing functions
- [ ] Test data cleaning with edge cases
- [ ] Validate data transformations
- [ ] Test duplicate removal logic
- [ ] Performance testing with PySpark
- **Deliverable:** Processing tests + performance report

#### Student C Tasks:
- [ ] Write database integration tests
- [ ] Verify referential integrity
- [ ] Test query performance
- [ ] Validate all relationships (author-quote, quote-tag)
- [ ] Create comprehensive test queries
- **Deliverable:** Database tests + query examples

---

### Days 12-13 (Documentation & Refinement)

#### Student A Tasks:
- [ ] Document web scraping module (docstrings, comments)
- [ ] Create scraper configuration guide
- [ ] Write troubleshooting section for scraping issues
- [ ] Add code examples for scraper usage
- [ ] Review and refactor code for PEP 8 compliance
- **Deliverable:** Scraper documentation

#### Student B Tasks:
- [ ] Document PySpark processing module
- [ ] Create data processing flow diagrams
- [ ] Document schema transformations
- [ ] Add configuration examples for PySpark
- [ ] Review and refactor code for best practices
- **Deliverable:** Processing documentation

#### Student C Tasks:
- [ ] Create comprehensive README.md
- [ ] Document database schema (tables, relationships, indexes)
- [ ] Write setup and installation instructions
- [ ] Create requirements.txt with all dependencies
- [ ] Document environment variables and configuration
- [ ] Create example usage guide
- **Deliverable:** Complete project documentation

---

### Day 14 (Final Testing & Submission Preparation)

#### All Students (Collaborative):
- [ ] Final end-to-end testing of complete pipeline
- [ ] Review all documentation for completeness
- [ ] Prepare demonstration queries
- [ ] Export database sample data
- [ ] Create project presentation/demo
- [ ] Final code review and cleanup
- [ ] Package all deliverables
- **Deliverable:** Final submission package

---

## Daily Sync-Up Schedule

**Daily Stand-ups (15 minutes):**
- Each student reports: What I completed yesterday, what I'm doing today, any blockers
- Recommended time: 9:00 AM or start of day

**End of Week 1 Review (1 hour):**
- Demo individual components
- Discuss integration challenges
- Adjust Week 2 tasks if needed

**Mid-Week 2 Check-in (30 minutes):**
- Verify integration status
- Review testing progress
- Coordinate documentation efforts

---

## Critical Dependencies

### Student B depends on Student A:
- **Day 3-4:** Needs sample scraped data for testing
- **Day 5-7:** Needs full dataset for processing

### Student C depends on Student B:
- **Day 3-4:** Needs schema design input
- **Day 5-7:** Needs processed data for database testing

### Integration Points:
- **Day 7:** All modules should be individually complete
- **Day 8-9:** Integration work begins
- **Day 14:** Final integrated system ready

---

## Risk Mitigation

### Potential Risks:

1. **Website Unavailability**
   - Mitigation: Student A should scrape data early and save backup
   - Student B and C can work with saved data

2. **PySpark Setup Issues**
   - Mitigation: Student B prioritizes environment setup in Days 1-2
   - Alternative: Use Docker for consistent environment

3. **Integration Delays**
   - Mitigation: Define clear interfaces early (Days 1-2)
   - Buffer time allocated in Days 8-9

4. **Database Performance Issues**
   - Mitigation: Student C implements indexes early
   - Test with small datasets first

---

## Success Criteria

### By End of Week 1:
- ✅ All three modules independently functional
- ✅ Sample data successfully flows through each component
- ✅ Database schema validated with test data

### By End of Week 2:
- ✅ Complete pipeline runs end-to-end successfully
- ✅ All ~100 quotes scraped and stored in database
- ✅ All tests passing
- ✅ Complete documentation
- ✅ Ready for demonstration

---

## Communication Protocol

### Slack/Discord Channels:
- **#general:** Overall project coordination
- **#scraper:** Student A updates and issues
- **#processing:** Student B updates and issues
- **#database:** Student C updates and issues
- **#integration:** Integration discussions (Week 2)

### Code Repository:
- Use Git with feature branches
- Branch naming: `feature/scraper`, `feature/processing`, `feature/database`
- Daily commits with meaningful messages
- Code reviews before merging to main

### File Sharing:
- **Student A:** Commits scraped data to `data/raw/`
- **Student B:** Commits processed data to `data/processed/`
- **Student C:** Commits database scripts to `database/`

---

## Technical Specifications Summary

### Student A - Scraper Module:
- **Language:** Python 3.8+
- **Libraries:** BeautifulSoup4, Requests
- **Output:** JSON files with metadata
- **Config:** URL, delay, user-agent, output path

### Student B - Processing Module:
- **Language:** Python 3.8+
- **Framework:** PySpark 3.x
- **Input:** JSON files from Student A
- **Output:** Processed DataFrames ready for DB
- **Config:** Spark settings, schema definitions

### Student C - Database Module:
- **Database:** PostgreSQL (or MySQL/SQLite)
- **ORM/Connector:** PySpark JDBC or psycopg2
- **Schema:** Normalized (authors, quotes, tags, quote_tags tables)
- **Config:** Database credentials, connection settings

---

## Deliverables Checklist

### Code:
- [ ] Web scraping module (Student A)
- [ ] PySpark processing module (Student B)
- [ ] Database storage module (Student C)
- [ ] Main pipeline orchestrator (Student C)
- [ ] Configuration files (All)
- [ ] requirements.txt (Student C)

### Database:
- [ ] SQL DDL scripts (Student C)
- [ ] Sample queries (Student C)
- [ ] Database backup/export (Student C)

### Documentation:
- [ ] README.md (Student C, reviewed by all)
- [ ] Code docstrings (All students for their modules)
- [ ] Database schema diagram (Student C)
- [ ] Setup instructions (Student C)
- [ ] Usage examples (All)

### Testing:
- [ ] Scraper tests (Student A)
- [ ] Processing tests (Student B)
- [ ] Database tests (Student C)
- [ ] Integration tests (All)

### Demonstration:
- [ ] Sample scraped data
- [ ] Working pipeline execution
- [ ] Database queries showing results
- [ ] Presentation/demo slides (All)

---

## Evaluation Alignment

### Functionality (40%) - All Students:
- Scraper extracts all quotes correctly (Student A: 15%)
- PySpark processes data correctly (Student B: 15%)
- Database stores and retrieves data (Student C: 10%)

### Code Quality (25%):
- Student A: 8% (Scraper code quality)
- Student B: 9% (Processing code quality)
- Student C: 8% (Database code quality)

### Database Design (20%):
- Student C: Primary (15%)
- Student B: Support (5% - schema input)

### Documentation (10%):
- Student C: Primary (README, setup) - 5%
- All Students: Code documentation - 5%

### Technical Implementation (5%):
- Student A: 1.5% (Web scraping best practices)
- Student B: 2% (PySpark usage)
- Student C: 1.5% (Database implementation)

---

## Final Notes

1. **Start Early:** Don't underestimate setup time
2. **Communicate Often:** Daily updates are critical
3. **Test Continuously:** Don't wait until integration to test
4. **Document as You Go:** Don't leave documentation for the end
5. **Ask for Help:** Use resources when stuck
6. **Back Up Your Work:** Commit code daily
7. **Review Each Other's Code:** Catch issues early

**Good luck with the project!**
