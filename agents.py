from crewai import Agent
from textwrap import dedent
import os
from search_tools import SearchTools
from summarise_tools import SummariseTools
from langchain_groq import ChatGroq

llm=ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="mixtral-8x7b-32768",
)

class BloodAgents:
    def __init__(self):
        pass

    def blood_report_summariser_expert(self):
        return Agent(
            role="Blood Report Summarization Expert",
            goal=f"""
                Summarise the blood report provided by finding all normal and abnormal values from the blood report

                Given a blood report that contains various categories of blood along with their values, the reference range may or may not be given,
                detect whether the category value lies in the reference range, if provided, or verify from the internet, and then finally
                create a summarised report that tells all the values that are normal in the blood and all the values that are abnormal.
                """,
            backstory="""
                Your role as a Blood Report Summarizer involves providing comprehensive information 
                about a person's blood, covering both normal and abnormal values detected in their blood 
                test report. You're tasked with relaying all relevant details to aid in understanding 
                the individual's blood report.
                """,
            tools=[
                SearchTools.search_internet,
                SummariseTools.summarize_text
                ],
            verbose=True,
            llm=llm,
            max_iter=2,
        )

    def expert_health_recommender(self):
        return Agent(
            role="Expert Health Recommender",
            goal=f"""
                Your objective is to furnish a detailed summary encompassing both normal and abnormal 
                values found in the blood report. This summary should also include health recommendations 
                tailored to address any abnormalities detected, along with links to articles providing 
                further insights and explanations.
                """,
            backstory=f"""
                As an Expert health Recommender you understand blood reports and figure out 
                which values are normal and which are not. You know about different types of blood 
                measurements and the ranges they should fall within. If the report doesn't give the 
                ranges, you'll find them online. Your main aim is to make a summary that shows all 
                the normal and abnormal values.
                """,
            tools=[
                SearchTools.search_internet,
                SummariseTools.summarize_text
                ],
            verbose=True,
            max_iter=2,
            llm = llm,
        )
