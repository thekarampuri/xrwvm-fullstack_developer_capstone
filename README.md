# Cars Dealership Review Application

## Full Stack Developer Capstone Project

### Project Overview
The **Cars Dealership Review Application** is a comprehensive, responsive full-stack web application designed for a national car retailer in the United States. The platform enables prospective car buyers and dealership visitors to browse dealership branches across all U.S. states, explore dealer details, view customer reviews with automated sentiment analysis, and register/log in to submit verified dealership reviews.

### Architecture & Tech Stack
- **Frontend**: React.js single-page application with React Router, Bootstrap 5, and responsive custom CSS styling.
- **Backend Application Server**: Django 4.2 framework exposing RESTful API endpoints for user authentication (session/token auth), dealer data proxying, review dispatching, and car inventory management.
- **Relational Database**: SQLite / Django ORM managing `CarMake` and `CarModel` entities with Django Admin integration.
- **Dealership & Reviews Microservice**: Node.js & Express service interacting with MongoDB / Mongoose for storing and querying dealership branches and customer reviews.
- **Sentiment Analysis Microservice**: Python Flask microservice leveraging NLTK VADER (`SentimentIntensityAnalyzer`) to classify customer review sentiments into positive, neutral, or negative categories.
- **Continuous Integration / Continuous Deployment (CI/CD)**: GitHub Actions automated workflow for linting, code validation, and quality assurance.
- **Containerization & Deployment**: Docker container definitions, Kubernetes manifests, and IBM Cloud Code Engine deployment configurations.

---

### Project Structure
```
├── .github/workflows/          # GitHub Actions CI/CD workflows
├── server/
│   ├── manage.py               # Django management script
│   ├── requirements.txt        # Python backend dependencies
│   ├── djangoproj/             # Django project configuration (settings, urls)
│   ├── djangoapp/              # Core Django application
│   │   ├── models.py           # CarMake and CarModel database models
│   │   ├── admin.py            # Django Admin registration and inlines
│   │   ├── views.py            # API views (auth, dealers, reviews, cars)
│   │   ├── urls.py             # Route definitions for djangoapp
│   │   ├── restapis.py         # Helper functions to consume microservices
│   │   ├── populate.py         # Initial data loader for car makes & models
│   │   └── microservices/      # Sentiment analysis microservice (Flask + NLTK)
│   ├── database/               # Dealerships & Reviews Express microservice
│   │   ├── app.js              # Express API endpoints
│   │   ├── dealership.js       # Dealership Mongoose schema
│   │   ├── review.js           # Review Mongoose schema
│   │   └── data/               # Seed data for dealerships and reviews
│   └── frontend/               # React client application and static assets
│       ├── static/             # Static HTML pages (Home, About Us, Contact Us)
│       └── src/                # React components (Login, Register, Dealers, Review)
└── submission_evidence/        # Coursera final submission artifacts and outputs
```

---

### Setup and Running Locally

1. **Install Python Dependencies**:
   ```bash
   pip install -r server/requirements.txt
   ```

2. **Run Dealership & Reviews Express Microservice**:
   ```bash
   cd server/database
   npm install
   node app.js
   ```
   *Runs on port 3030.*

3. **Run Sentiment Analyzer Flask Microservice**:
   ```bash
   cd server/djangoapp/microservices
   python app.py
   ```
   *Runs on port 5050.*

4. **Build the React Frontend**:
   ```bash
   cd server/frontend
   npm install
   npm run build
   ```

5. **Run Django Backend & Application Server**:
   ```bash
   cd server
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver 8000
   ```
   *Access the application at `http://localhost:8000`.*