from crewai import Task

class BloodTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def blood_analysis(self, agent, text):
        return Task(
            description=f"""
                Analyze the blood report and provide a summary to the user
                
                - The report will contain various categories related to blood with defined values.
                - Determine if each category's value is within the normal range.
                - If the normal range is provided, compare the value to it; otherwise, search the internet to determine if the value is normal for a human.
                - Summarize the report, indicating which categories are normal and which are abnormal.
            """,
            agent=agent,
            expected_output=f"Summarized Blood Report",
            async_execution=False,
        )

    def health_checker(self, agent, text):
        return Task(
            description=f"""
                Revise the summary provided, focusing on abnormal values.
                
                - Search the internet for articles regarding detected abnormalities and health recommendations to address them.
                - Return links to articles discussing the detected abnormalities, health recommendations, and links of supporting articles.
            """,
            agent=agent,
            expected_output=f"List of Health Recommendations and Supporting Articles Links",
            async_execution=False,
        )