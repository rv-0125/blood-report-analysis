import os
from dotenv import load_dotenv
from crewai import Operator, Agent, Task, Crew
from pdf_to_text import pdf_to_text
from tools.search_tools import SearchTools
from tools.summarise_tools import SummariseTools
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool,
    PDFSearchTool
)
from langchain_groq import ChatGroq
from textwrap import dedent

# Load environment variables from .env file
load_dotenv()

# Set up API keys
serper_api_key = os.getenv("SERPER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model="mixtral-8x7b-32768",
)
# Instantiate tools
docs_tool = DirectoryReadTool(directory=r'C:\Users\SURFACE\Desktop\wingify_final_submission')
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()
pdf_read_tool = PDFSearchTool()

# Create agents
class HealthAgents:
    def __init__(self):
        pass

    def blood_report_analyzer(self):
        return Agent(
            role='Blood Report Analyzer',
            goal="""
                Analyze the provided blood test report to identify and summarize key health indicators and findings. Determine normal and abnormal values based on given ranges or verified internet sources.
                """,
            backstory="""
                You are an experienced Blood Report Analyzer. Your expertise lies in interpreting blood test results to provide actionable insights regarding a person's health status.
                """,
            tools=[file_tool, pdf_read_tool, docs_tool],
            llm=llm,
            verbose=True,
            max_iter=2,
        )

    def health_advisor(self):
        return Agent(
            role='Health Advisor',
            goal="""
                Provide health recommendations based on the summarized blood report findings. Include relevant articles and URLs to support the recommendations.
                """,
            backstory="""
                You are a proficient Health Advisor. You use your knowledge to integrate medical data and online resources to give practical health advice, always citing sources for any recommendations made.
                """,
            tools=[search_tool, web_rag_tool, docs_tool, file_tool],
            llm=llm,
            verbose=True,
            max_iter=2,
        )

class HealthTasks:
    def analyze_blood_report(self, agent, text):
        return Task(
            description="""
                Analyze the provided blood test report to identify and summarize key health indicators. Determine if values are within normal ranges or identify abnormalities.
                """,
            expected_output='Summarized Blood Report',
            agent=agent,
            async_execution=False,
        )

    def generate_health_recommendations(self, agent, context):
        return Task(
            description="""
                Based on the summarized blood report, provide health recommendations. Include URLs to articles that support the recommendations.
                """,
            expected_output='Health Recommendations with URLs',
            agent=agent,
            context=[context],
            async_execution=False,
        )

# Main BloodCrew class
class BloodCrew:
    def __init__(self, text):
        self.text = text

    def run(self):
        agents = HealthAgents()
        tasks = HealthTasks()

        blood_report_analyzer = agents.blood_report_analyzer()
        health_advisor = agents.health_advisor()

        analyze_blood_report_task = tasks.analyze_blood_report(
            blood_report_analyzer,
            self.text
        )

        generate_health_recommendations_task = tasks.generate_health_recommendations(
            health_advisor,
            analyze_blood_report_task
        )

        crew = Crew(
            agents=[blood_report_analyzer, health_advisor],
            tasks=[analyze_blood_report_task, generate_health_recommendations_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result

# Main execution
if __name__ == "__main__":
    print("## Welcome to the Blood Report Analysis Crew")
    print('----------------------------------------')
    
    valid_input = False

    while not valid_input:
        input_type = input(dedent("""
            Do you want to upload a PDF or provide text for the blood report?
            Type 'pdf' for PDF or 'text' for text: """)).lower()

        if input_type == 'pdf':
            pdf_path = input(dedent("""
                Please provide the path to the PDF file: """))

            tables = pdf_read_tool.read_pdf(pdf_path)

            if tables:
                blood_report_text = pdf_to_text(tables)
                print(blood_report_text)
                valid_input = True
            else:
                print("Failed to extract tables from the PDF. Please try again.")
        
        elif input_type == 'text':
            blood_report_text = input(dedent("""
                Please provide the text of the blood report: """))

            valid_input = True

        else:
            print("Invalid input. Please type 'pdf' or 'text'.")

    blood_crew = BloodCrew(blood_report_text)
    result = blood_crew.run()

    print("\n\n########################")
    print("## Here is your Blood Report Analysis")
    print("########################\n")
    print(result)
