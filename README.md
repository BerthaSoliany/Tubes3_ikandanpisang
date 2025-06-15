# Tubes3_ikandanpisang

## Table of Content
1. [About](#about)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [How To Run](#how-to-run)
5. [Setting Up the Database](#setting-up-the-database)
6. [Author](#author)

## About
The CV Analyzer App is designed to analyze CVs using advanced algorithms and provide insights based on the extracted information. The application utilizes the Knuth-Morris-Pratt (KMP), Boyer-Moore (BM), and Aho-Corasick algorithms for efficient string searching, along with the Levenshtein Distance algorithm for measuring string similarity which handles possible typo. Regular Expressions (Regex) are employed to extract important information from CVs to create summary automatically.

| Algorithm | Explanation |
|------|-----|
| **Knuth-Morris-Pratt** algorithm | focuses on avoiding redundant character re-checks after a mismatch, implemented using border function which determines how much should pattern be shifted after a mismatch instead of repeating from the beginning. | 
| **Boyer-Moore** algorithm | compares pattern from right to left instead of the usual left to right, implemented using looking-glass and character-jump technique based on the last occurrence of each letter in the pattern. |
| **Aho-Corasick** algorithm | preprocessed all patterns to build an automaton, which consists of a trie structure of all possible prefixes, failure-links, dan output-links, allowing simultaneous searching of numerous pattens within one traversal of text. |
| **Levenshtein Distance** algorithm | calculates the mininum number of character edits (insertions, deletions, or substitutions) required to transform one string into another. |
| **Regular Expressions** | standardized text patterns to match and extract spesific information from text. |

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
├── pyproject.toml             # Project configuration
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
> If you have trouble activating the venv, please locate the activate file in the .venv folder and update the path accordingly.
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
