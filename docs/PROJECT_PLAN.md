# Customer Churn & LTV Engine — 12 Week Project Plan

## Project Duration

12 Weeks / 3 Months

## Project Objective

The objective of this project is to develop a complete customer analytics and
retention intelligence platform capable of identifying customers at risk of
churn, estimating customer lifetime value, prioritizing customers for
retention actions, and exposing predictions through an API and interactive
dashboard.

---

# Month 1 — Data Engineering & Machine Learning

## Week 1 — Environment Setup, Data Ingestion & EDA

### Tasks
- Set up Python development environment
- Configure project structure
- Install required dependencies
- Obtain and validate Telco Customer Churn dataset
- Implement data ingestion pipeline
- Analyze dataset structure
- Analyze missing values
- Analyze duplicate records
- Analyze categorical and numerical variables
- Perform exploratory data analysis
- Identify major churn patterns

### Deliverables
- Dataset ingestion script
- EDA notebook
- Initial business insights

---

## Week 2 — Data Cleaning & Feature Engineering

### Tasks
- Convert TotalCharges to numeric format
- Handle missing values
- Remove unnecessary customer identifiers
- Encode churn target
- Create customer tenure groups
- Calculate average monthly revenue
- Create monthly-to-total revenue ratio
- Create long-term customer indicator
- Create high monthly charge indicator

### Deliverables
- Preprocessing pipeline
- Feature engineering pipeline
- Cleaned dataset
- Final feature dataset

---

## Week 3 — Churn Prediction Models

### Tasks
- Prepare training and testing datasets
- Build preprocessing pipeline
- Train Logistic Regression model
- Train Random Forest model
- Train XGBoost model
- Evaluate model performance
- Compare accuracy, precision, recall and F1-score
- Select the best performing model

### Deliverables
- Trained churn models
- Model comparison results
- Selected production churn model

---

## Week 4 — Model Explainability

### Tasks
- Integrate SHAP explainability
- Analyze global feature importance
- Identify major churn drivers
- Generate SHAP summary visualization
- Generate feature importance report
- Translate model findings into business insights

### Deliverables
- SHAP analysis
- Feature importance report
- Churn driver analysis

---

# Month 2 — Customer Value, Database & API

## Week 5 — Customer Lifetime Value Engine

### Tasks
- Design estimated LTV methodology
- Calculate average monthly revenue
- Estimate customer lifetime
- Generate predicted LTV
- Create LTV segments
- Evaluate LTV model
- Document limitations of the available dataset

### Deliverables
- LTV prediction engine
- LTV predictions
- LTV segmentation

---

## Week 6 — Customer Priority & Retention Engine

### Tasks
- Combine churn probability and predicted LTV
- Identify high-risk customers
- Identify high-value customers
- Identify critical customers
- Develop customer priority rules
- Generate retention target list

### Deliverables
- Customer priority engine
- Customer priority dataset
- Retention target list

---

## Week 7 — PostgreSQL Integration

### Tasks
- Configure PostgreSQL
- Create project database
- Design relational database schema
- Create customer table
- Create churn prediction table
- Create LTV prediction table
- Create customer priority table
- Build Python database connection
- Load analytics data into PostgreSQL

### Deliverables
- PostgreSQL database
- Database schema
- Data loading pipeline

---

## Week 8 — SQL Analytics & FastAPI

### Tasks
- Develop SQL business analytics queries
- Analyze churn by contract
- Analyze churn by internet service
- Analyze churn by tenure
- Identify high-risk customers
- Identify high-LTV customers
- Develop retention target queries
- Build FastAPI application
- Create churn prediction endpoint
- Create LTV prediction endpoint
- Create customer priority endpoint
- Test API using Swagger

### Deliverables
- SQL analytics layer
- FastAPI backend
- API endpoints
- Swagger API testing

---

# Month 3 — Dashboard & Production Readiness

## Week 9 — Streamlit Dashboard

### Tasks
- Design dashboard layout
- Connect dashboard to PostgreSQL
- Create business KPI cards
- Create churn visualizations
- Create tenure analysis
- Create priority distribution
- Create LTV segmentation
- Display critical customers
- Display high-risk customers
- Display high-value customers

### Deliverables
- Streamlit analytics dashboard

---

## Week 10 — Interactive Prediction Application

### Tasks
- Build customer input form
- Connect Streamlit to FastAPI
- Implement real-time churn prediction
- Implement LTV prediction
- Implement LTV segmentation
- Implement customer priority prediction
- Test multiple customer profiles
- Improve dashboard usability

### Deliverables
- Interactive prediction interface
- End-to-end prediction workflow

---

## Week 11 — Testing & Optimization

### Tasks
- Test data pipeline
- Test database connectivity
- Test ML prediction pipeline
- Test FastAPI endpoints
- Test dashboard
- Validate model outputs
- Test invalid API inputs
- Review error handling
- Review project dependencies
- Review GitHub repository structure
- Optimize code where required

### Deliverables
- Testing results
- Stable end-to-end application
- Clean project structure

---

## Week 12 — Documentation & Finalization

### Tasks
- Prepare project README
- Document architecture
- Document API endpoints
- Document ML methodology
- Document LTV methodology
- Document business insights
- Document project limitations
- Document future improvements
- Review `.gitignore`
- Review GitHub repository
- Final code review
- Final project demonstration

### Deliverables
- Complete GitHub repository
- Technical documentation
- API documentation
- Architecture documentation
- Final project report

---

# Final Project Deliverables

- Python data pipeline
- Exploratory data analysis
- Feature engineering pipeline
- Churn prediction models
- SHAP explainability
- LTV estimation engine
- Customer priority engine
- PostgreSQL database
- SQL analytics
- FastAPI prediction service
- Streamlit dashboard
- Interactive customer prediction
- Technical documentation
- API documentation
- Project architecture

---

# Technology Stack

Python  
Pandas  
NumPy  
Scikit-learn  
XGBoost  
SHAP  
PostgreSQL  
SQLAlchemy  
FastAPI  
Streamlit  
Plotly  
Git & GitHub