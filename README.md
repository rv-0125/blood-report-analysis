# Blood Report Analysis Crew

## Approach to the Task

1. **Setting Up the Environment:**
   - The environment is configured using environment variables stored in an `.env` file to keep sensitive information secure.

2. **Defining and Initializing Tools:**
   - Necessary tools are initialized, including those for reading PDFs, text documents, and accessing web resources.
   - API services like SerperDevTool are integrated for internet searches.

3. **Creating the Agent:**
   - Agents are defined with specific roles, goals, and backstories to ensure they perform their tasks accurately.
   - Tools and language models are assigned to the agents to enhance their capabilities.

4. **Defining Tasks and Crew:**
   - Detailed tasks are created for analyzing blood reports and providing health recommendations.
   - The crew configuration is set up with the defined agents and tasks.

5. **Executing the Task:**
   - The crew process is kicked off to analyze the blood report and generate health recommendations.

## Steps to Run the Code

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/blood-report-analysis.git
   cd blood-report-analysis
