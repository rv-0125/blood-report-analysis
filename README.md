# Blood Report Analysis Crew

## Overview
This project aims to analyze blood test reports and provide health recommendations based on the findings. The solution leverages advanced language models and integrated tools to extract, analyze, and summarize data from blood reports, and subsequently offer practical health advice supported by credible sources.

## Approach to the Task

### Setting Up the Environment:
- Configured necessary environment variables for API keys.
- Initialized tools required for reading files, processing PDFs, and searching the web.

### Defining and Initializing Tools:
- Integrated tools such as DirectoryReadTool, FileReadTool, PDFSearchTool, SerperDevTool, and WebsiteSearchTool.
- Utilized the `pdf_to_text` function to convert PDF content to text.

### Creating the Agents:
- **Blood Report Analyzer:** Analyzes blood test reports to summarize key health indicators and findings.
- **Health Advisor:** Provides health recommendations based on the summarized report, including URLs to relevant articles.

### Handling Unauthorized Errors:
- Ensured all API keys were valid and had the required permissions to avoid unauthorized access errors.

### Defining Tasks and Crew:
- Created tasks for analyzing blood reports and generating health recommendations.
- Set up a sequential process model for task execution.

### Executing the Task:
- Provided an interactive prompt for the user to upload a PDF or input text directly.
- Used the PDFSearchTool and `pdf_to_text` for PDFs, and accepted direct text inputs.
- The agents executed their respective tasks and provided a comprehensive analysis and health advice.

## Steps to Run the Code

### Prerequisites
- Python 3.8 or higher
- Necessary API keys for SERPER_API_KEY and GROQ_API_KEY
- Required Python packages (install using the provided `requirements.txt` file)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/blood-report-analysis.git
    cd blood-report-analysis
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Code

1. **Set up environment variables:**
    ```bash
    export SERPER_API_KEY="your_serper_api_key"
    export GROQ_API_KEY="your_groq_api_key"
    ```

2. **Run the main script:**
    ```bash
    python main.py
    ```

3. **Follow the prompts:**
    - You will be asked whether you want to upload a PDF or provide text for the blood report.
    - For PDFs, provide the path to the PDF file.
    - For text, input the text of the blood report directly.

4. **View the results:**
    - The output will display a comprehensive analysis of the blood report and health recommendations with URLs to relevant articles.
