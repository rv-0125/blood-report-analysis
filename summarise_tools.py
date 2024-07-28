import json
import os
import requests
from langchain.tools import tool
from summarizer import Summarizer  # Assuming you have already installed the bert-extractive-summarizer library

class SummariseTools():
    @tool("Summarize Text")
    def summarize_text(text):
        """Summarize the given text"""
        model = Summarizer()  # Use the imported Summarizer class
        summary = model(text, ratio=0.5)  # Adjust ratio for desired summary length
        return summary