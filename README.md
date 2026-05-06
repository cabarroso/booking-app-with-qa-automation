# Booking App with QA Automation Framework

A full-stack booking application paired with a scalable end-to-end QA automation framework built using Python, FastAPI, React, Pytest, and Playwright.

This project was designed to simulate a real-world software testing environment by combining:

* a custom-built booking application
* API and UI automation
* CI/CD integration
* reusable testing architecture
* containerized execution

The goal of this project is to demonstrate practical QA automation engineering skills beyond tutorial-level testing.

---

# Project Overview

This repository contains two major components:

## 1. Full-Stack Booking Application

A custom booking platform with:

* React frontend
* FastAPI backend
* REST API
* database persistence
* authentication support

Users can:

* create bookings
* view bookings
* delete bookings

---

## 2. QA Automation Framework

A reusable automation framework designed to test the booking application through:

* UI automation
* API automation
* integration workflows
* validation utilities
* CI pipelines

The framework emphasizes:

* maintainability
* scalability
* reusable abstractions
* realistic testing workflows

---

# Tech Stack

## Frontend

* React
* Vite
* Axios

## Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite

## QA Automation

* Pytest
* Playwright
* Requests
* Faker
* pytest-xdist

## DevOps / Tooling

* Docker
* Docker Compose
* GitHub Actions

---

# Features

## Booking Application

* User login
* Create booking
* View bookings
* Update booking
* Delete booking
* API-driven frontend communication
* Persistent database storage

---

## Automation Framework

* API testing
* UI testing
* Page Object Model architecture
* reusable fixtures
* service layer abstraction
* parametrized testing
* parallel execution support
* logging utilities
* environment configuration support
* CI/CD integration

---

# Architecture

```text id="s4iuhs"
Frontend (React)
        ↓
Backend API (FastAPI)
        ↓
Database (SQLite)

Automation Framework
├── API Tests
├── UI Tests
├── Fixtures
├── Page Objects
├── Services
└── Utilities
```

---

# Project Structure

```text id="jlwmcc"
project/
│
├── backend/
│   ├── app/
│       ├── models/
│       ├── routes/
│       ├── schemas/
│       └── database
│
├── frontend/
│
├── framework/
│   ├── services/
│   ├── utils/
│   └── fixtures/
│
├── tests/
│   ├── api/
│   ├── ui/
│   └── integration/
│
├── pages/
│
├── logs/
├── allure-results/
│
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash id="u06sln"
git clone https://github.com/cabarroso/booking-app-with-qa-automation
cd booking-app-with-qa-automation
```

---

# Backend Setup

Create virtual environment:

```bash id="a5fopk"
python -m venv venv
```

Activate environment:

### Windows

```bash id="egltxa"
venv\Scripts\activate
```

### Mac/Linux

```bash id="0tvn8d"
source venv/bin/activate
```

Install dependencies:

```bash id="otof00"
pip install -r requirements.txt
```

---

# Frontend Setup

```bash id="j6wxtr"
cd frontend
npm install
```

Run frontend:

```bash id="8drk77"
npm run dev
```

---

# Running the Backend

```bash id="ut7f5d"
uvicorn app.main:app --reload
```

---

# Running Tests

Run all tests:

```bash id="7xt1d2"
pytest
```

Run API tests:

```bash id="1qjlwm"
pytest tests/api
```

Run UI tests:

```bash id="bvy0b8"
pytest tests/ui
```

Run tests in parallel:

```bash id="pkzqjp"
pytest -n auto
```

---

# Docker Execution

Run the full application stack:

```bash id="2n4g6w"
docker compose up --build
```

Run automated tests inside containers:

```bash id="2zx7ku"
docker compose run --rm tests pytest
```

---

# CI/CD

GitHub Actions automatically:

* installs dependencies
* builds containers
* executes automated tests
* validates pull requests

---

# Example Test Coverage

## API Testing

* authentication validation
* CRUD operations
* negative test scenarios
* response validation
* status code verification

---

## UI Testing

* login flows
* booking creation
* form validation
* booking deletion
* navigation workflows

---

## Integration Testing

* create booking via API and validate in UI
* end-to-end workflow validation
* cross-layer verification

---

# Design Patterns & Practices

This project uses:

* Page Object Model (POM)
* service layer abstraction
* reusable Pytest fixtures
* environment-based configuration
* centralized logging
* modular test architecture

---

# Environment Variables

Example `.env`:

```env id="5g8s0z"
BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

---

# Future Improvements

* Allure reporting
* database validation testing
* visual regression testing
* performance/load testing
* cross-browser execution
* role-based authentication testing

---

# Why This Project Exists

This project was created to practice and demonstrate:

* full-stack application development
* QA automation architecture
* UI and API testing
* CI/CD workflows
* scalable automation design
* realistic testing practices

---

# Author

Built by [Your Name]

GitHub: [Your GitHub Profile]

---

# License

This project is for educational and portfolio purposes.
