from crewai import Crew, Process, Agent, Task
from textwrap import dedent
from agents import BloodAgents
from tasks import BloodTasks
import tabula
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

def extract_tables_from_pdf(pdf_path):
    """Extracts tables from the first page of a PDF using Tabula."""
    try:
        # Extract tables from the first page
        tables = tabula.read_pdf(pdf_path, pages=1, multiple_tables=True)
        print(tables)
        return tables
    except Exception as e:
        print(f"Error occurred while extracting tables from PDF: {e}")
        return None

def convert_table_to_text(tables):
    """Converts the extracted tables into a readable text format."""
    text = ""
    header_printed = False  # Flag to track if the header is printed
    for table in tables:
        # Check if the table is not empty
        if not table.empty:
            if not header_printed:
                text += table.columns[0] + ": "
                header_printed = True
                text += "\n"
            for _, row in table.iterrows():
                # Check if the row contains at least one non-null value
                if not row.isnull().all():
                    # Initialize a flag to keep track of whether the column name is printed
                    printed_column_name = False
                    # Iterate through the columns
                    for idx, value in enumerate(row):
                        # Check if the value is not null
                        if pd.notnull(value):
                            # If the column has a name and it has not been printed yet, append the name
                            if table.columns[idx] != 'Unnamed: 0' and not printed_column_name:
                                text += table.columns[idx] + ": "
                                printed_column_name = True
                            # Append the value to the text
                            text += str(value) + " "
                    # Add a newline after processing each row
                    text += "\n"
    
    return text.strip()

class BloodCrew:
    def __init__(self, text):
        self.text = text

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = BloodAgents()
        tasks = BloodTasks()

        # Define your custom agents and tasks here
        blood_report_summariser_expert = agents.blood_report_summariser_expert()
        expert_health_recommender = agents.expert_health_recommender()

        blood_analysis = tasks.blood_analysis(
            blood_report_summariser_expert,
            self.text
        )

        health_checker = tasks.health_checker(
            expert_health_recommender,
            self.text
        )

        # Define your custom crew here
        crew = Crew(
            agents=[blood_report_summariser_expert,
                    expert_health_recommender
                    ],
            tasks=[
                blood_analysis,
                health_checker
            ],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to Blood Report Analyzer Crew")
    print('----------------------------------------')
    
    # Initialize flag for valid input
    valid_input = False

    while not valid_input:
        # Ask the user whether to upload PDF or provide text
        input_type = input(dedent("""
            Do you want to upload a PDF or provide text for the blood report?
            Type 'pdf' for PDF or 'text' for text: """)).lower()

        # Check the user's input and proceed accordingly
        if input_type == 'pdf':
            # Prompt the user to provide the path to the PDF file
            pdf_path = input(dedent("""
                Please provide the path to the PDF file: """))

            # Attempt to convert the PDF to text
            tables = extract_tables_from_pdf(pdf_path)

            if tables:
                blood_report_text = convert_table_to_text(tables)
                print(blood_report_text)
                valid_input = True
            else:
                print("Failed to extract tables from the PDF. Please try again.")
        
        elif input_type == 'text':
            # Prompt the user to provide the text of the blood report
            blood_report_text = input(dedent("""
                Please provide the text of the blood report: """))

            valid_input = True

        else:
            print("Invalid input. Please type 'pdf' or 'text'.")
    
    blood_crew = BloodCrew(blood_report_text)
    result = blood_crew.run()

    # Print the analysis result
    print("\n\n########################")
    print("## Here is your Blood Report Analysis")
    print("########################\n")
    print(result)