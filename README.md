# Tubes3_ikandanpisang

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

## How To
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
4. Install requirement
    ```
    pip install -r requirements.txt
    ```
5. run the flet app
    ```
    flet run main.py
    ```
> [!NOTE]
> Go to Flet docs for more info [Flet](https://flet.dev/docs/)

## Usage
- Upload CVs through the upload page.
- View analysis results on the results page.
- Refer to the project report in the `doc` folder for detailed insights and findings.