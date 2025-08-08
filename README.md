# PII Redactor

A simple project to redact Personally Identifiable Information (PII) from text. This repository provides a basic frontend and backend structure.

## Setup

### Backend

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv env
    ```
3.  Activate the environment:
    -   On Windows: `env\Scripts\activate`
    -   On macOS/Linux: `source env/bin/activate`
4.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Frontend

The frontend is a simple set of static files and does not require a build step.

## Run

1.  Run the backend server from the `backend` directory:
    ```bash
    python app.py
    ```
    The server will start on `http://localhost:5000`.

2.  Open the frontend:
    Open the `frontend/index.html` file in your web browser.

## Deploy

This project can be deployed using Docker.

1.  Build the Docker image from the root directory:
    ```bash
    docker build -t pii-redactor ./backend
    ```

2.  Run the Docker container:
    ```bash
    docker run -p 5000:5000 pii-redactor
    ```

## Git Commands

Here are some example commands to initialize this repository locally and push it to a new repository on GitHub.

1.  Initialize a new git repository in your local project folder:
    ```bash
    git init
    ```

2.  Add all files to the staging area:
    ```bash
    git add .
    ```

3.  Commit the files with a message:
    ```bash
    git commit -m "Initial commit: project structure setup"
    ```

4.  Add your remote repository on GitHub (replace with your actual URL):
    ```bash
    git remote add origin https://github.com/your-username/pii-redactor.git
    ```

5.  Push your local changes to the remote repository's `main` branch:
    ```bash
    git push -u origin main
    ```
