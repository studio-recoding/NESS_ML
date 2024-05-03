class Template:
    daily_email_template = """
                    {persona}
                    Construct an email to conclude the user's day. The email should:

                    Acknowledge the user's efforts and achievements throughout the day.
                    Offer encouragement and suggestions for preparing for tomorrow’s agenda.
                    Use this information to create a personalized, thoughtful email that reinforces positive feedback and provides motivational insights for the upcoming day.
                    You should construct the email based solely on the schedule provided, without assuming or extrapolating additional details.
                    YOU MUST USE {output_language} TO RESPOND. The length of the email should not exceed 2 paragraphs. Do not call user's name.

                    Today's schedule for the user1:
                    2021-07-19T09:00:00: Zoom meeting attendance
                    2021-07-19T11:00:00: Review of project report
                    2021-07-19T13:00:00: Business lunch
                    2021-07-19T15:00:00: Team meeting
                    2021-07-19T18:00:00: Workshop preparation

                    Email:
                    Today's activities show you managed a full and productive schedule.

                    In the morning, your active participation in the Zoom meeting was impressive. Such engagement is crucial for fostering collaborative success.
                    During your project report review, your attention to detail stood out. This meticulousness will significantly contribute to the project's success.
                    The business lunch was an important time for building relationships. Such networking will assist in future tasks.
                    In the afternoon, you effectively led the team meeting, playing a vital role in enhancing team cooperation.
                    Lastly, thank you for your effort in preparing for the workshop. This preparation will facilitate a smooth running of tomorrow's session.

                    Thank you for your hard work today. Rest well and recharge for another fruitful day tomorrow.

                    Today's schedule for the user2:
                    {schedule} 

                    Email:
                    """
