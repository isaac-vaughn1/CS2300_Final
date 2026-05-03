# Project Setup Guide

This project requires Python 3.x.x and Docker Desktop to run properly.

---

## Prerequisites

Before starting, ensure you have the following installed:

- Python 3.x.x (3.8+ recommended)
- Docker Desktop
- pip (comes with Python)

Verify installations:

```bash
python --version
docker --version
```

---

## Project Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-project-root>
```

---

### 2. Create a Virtual Environment

From the project root directory:

```bash
python -m venv venv
```

---

### 3. Activate the Virtual Environment

**Windows (PowerShell / CMD):**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

---

### 4. Install Dependencies

Make sure your virtual environment is activated:

```bash
pip install -r requirements.txt
```

---

## Database Setup (Docker)

This project uses a PostgreSQL container via Docker Compose.

### 5. Start PostgreSQL Container

From the project root directory:

```bash
sudo docker compose up -d
```

This starts the database in detached mode.

To verify it's running:

```bash
docker ps
```

---

## Run the Application

From the project root directory (with venv activated):

```bash
python src/main.py
```

---

## Stop the Database

Stop containers:

```bash
sudo docker compose down
```

Stop and remove volumes (full reset):

```bash
sudo docker compose down -v
```

---

## Important Note on Input Handling

This application assumes that **all user input is correctly formatted and valid for the most part**.

To avoid unnecessary errors or unexpected behavior, please ensure that all input provided to the program follows the expected format and constraints exactly as intended.

Invalid or incorrectly formatted input may lead to runtime errors or undefined behavior.

---

## Project Structure

```
.
├── src/
│   └── main.py
├── sql/
├── requirements.txt
├── docker-compose.yml
├── venv/
└── README.md
```

---

## Troubleshooting

### Python not found
Try:
```bash
python3 --version
```

### Recreate virtual environment
```bash
rm -rf venv
python -m venv venv
```

### Docker issues
- Make sure Docker Desktop is running
- On Windows/macOS, you usually do NOT need sudo

---

## Notes

- Always activate the virtual environment before running the app
- If dependencies change:
```bash
pip install -r requirements.txt
```
```
