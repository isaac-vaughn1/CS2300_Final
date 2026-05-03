# Project Setup Guide

This project requires Python 3.x.x and Docker Desktop to run properly.

---

## Prerequisites

Before starting, ensure you have the following installed:

- Python 3.x.x
- Docker Desktop
    - Docker Desktop is a GUI application that makes it easy to use Docker on most
        computer platforms. It includes everything you need to build, run, and manage containers
        on your computer.
        - macOS: https://docs.docker.com/desktop/setup/install/mac-install/
            - It is strongly recommended to install Docker Desktop via Homebrew. This will
            make updating and managing Docker much (a lot!) easier in the long run,
            especially when newer versions or patches are released.
        - Windows: https://docs.docker.com/desktop/setup/install/windows-install/
        - Linux: https://docs.docker.com/desktop/setup/install/linux/
- pip (comes with Python)

Verify installations:

```bash
python --version
docker --version
```

---

## Project Setup

### 1. Clone the Repository (If applicable)

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
├── sql/
│   └── 01_schema.sql
|   └── 02_sample_date.sql
├── src/
│   └── db_ops.py
│   └── main.py
│   └── menus.py
│   └── screen_logic.py
|
├── venv/
├── .gitignore
├── docker-compose.yml
└── README.md
├── requirements.txt
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
