# Tubes3_ikandanpisang

## Table of Content
1. [About](#about)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [How To Run](#how-to-run)
5. [Setting Up the Database](#setting-up-the-database)
6. [Author](#author)

## About
The CV Analyzer App is designed to analyze CVs using advanced algorithms and provide insights based on the extracted information. The application utilizes the Knuth-Morris-Pratt (KMP) and Boyer-Moore (BM) algorithms for efficient string searching, along with the Levenshtein Distance algorithm for measuring string similarity. Regular Expressions (Regex) are employed to extract important information from CVs automatically.

## Project Structure
```
Tubes3_ikandanpisang
├── src
│   ├── main.py                # Entry point of the application
│   ├── frontend               # Frontend components
│   │   ├── pages              # Page logic
│   │   ├── components         # UI components
│   ├── backend                # Backend logic
│   │   ├── database           # Database models and connection
│   │   ├── algorithms         # String searching algorithms
│   └── utils                  # Utility functions
├── data                       # Sample CV files for testing
├── doc                        # Project report
├── pyproject.toml            # Project configuration
├── requirements.txt           # Required Python packages
└── README.md                  # Project documentation
```

## Requirements
- IDE
- Git
- Python
- MySQL

## How To Run
1. Clone the repository
    ```bash
   git clone https://github.com/BerthaSoliany/Tubes3_ikandanpisang.git
   cd Tubes3_ikandanpisang
   ```
2. Make a venv
    ```
    py -m venv .venv
    ```
3. Activate the venv
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source 

> [!NOTE]
> If you can't active the venv, please try finding the activate file in the .venv folder and renew the path
4. Install requirement
    ```
    pip install -r requirements.txt
    ```
5. run the flet app
    ```
    flet run main.py
    ```

## Setting Up the Database
This is the step to step for setting up the seeding (connecting a personal information to a CV)
1. Open another terminal and go to the database folder
    ```bash
    cd src/backend/database
    ```
2. Run the seeding
    ```bash
    python seeding.py
    ```
3. Choose option 2 to clear the database and input 'y'
4. Choose option 1 to do the seeding

## Author
| Nama | Nim |
|------|-----|
| Bertha Soliany Frandi | 13523026 |
| Rafen Max Alessandro | 13523031 |
| Grace Evelyn Simon | 13523087 |