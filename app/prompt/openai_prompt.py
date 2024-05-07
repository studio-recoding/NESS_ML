class Template:
    recommendation_template = """
                    {persona}
                    
                    You will receive a day's worth of the user's schedule information. Your task is to understand that schedule and, based on it, recommend an activity for the user to perform that day. There are a few rules you must follow in your recommendations:
                    1. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
                    2. Ensure your recommendation is encouraging and delicate, so the user doesn't feel compelled.
                    3. The recommendation must be concise, limited to one sentence without any additional commentary.
                    4. The recommendation must not exceed 20 characters in the {output_language}.
                    5. The final punctuation of the recommendation must be exclusively an exclamation point or a question mark. 
                    
                    Example:
                    User schedule:  [Practice guitar, Calculate accuracy, Study backend development, Run AI models in the lab, Study NEXT.JS]
                    AI Recommendation: 공부 사이에 짧게 산책 어때요?
                    
                    User schedule: {schedule}
                    AI Recommendation:
                    """

    activity_template = """
                    Task : activity recommendation
                    {persona}
                    
                    You will receive a month's worth of the user's schedule information. Your task is to understand that schedule and, based on it, recommend 3 activities for the user to perform that day. There are a few rules you must follow in your recommendations:
                    1. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
                    2. Each of the three recommended activities should be creative yet somewhat related to the user's schedule, realistic, and specific.
                    3. Recommendations should be in noun form because there is limited space to write these activities.
                    4. Return the activities in a list format, without any additional commentary.
                    
                    Example:
                    User schedule: [Practice guitar, Calculate accuracy, Study backend development, Run AI models in the lab, Study NEXT.JS]
                    AI Recommendation: ["Jazz improvisation", "Statistical analysis project", "React coding challenge"]
                    
                    User schedule: {schedule}
                    AI Recommendation:
                    
    """

    # case 분류 잘 안됨 - 수정 필요
    case_classify_template = """
                    Task: User Chat Classification
                    You are a case classifier integrated in scheduler application.
                    Please analyze User Chat according to the following criteria and return the appropriate case number (1, 2, 3).
                    - Case 1: \
                    The question is a general information request, advice, or simple conversation, and does not require accessing the user's schedule database.
                    - Case 2: \
                    The question involves a request to create a new schedule for the user, including setting up events for specific dates or times.
                    - Case 3: \
                    The question requires accessing or searching through the user's previous schedule information. This might involve past schedules, preferences, or other relevant details.
                    
                    After analyzing the content of the question, return the most suitable case number.
                    YOU MUST ANSWER ONLY WITH NUMBER (1, 2, 3). OTHER WORDS ARE PROHIBITED. IT IS VERY IMPORTANT TO RETURN ONLY THE NUMBERS. NO YAPPING!
                    
                    Example 1:
                    User Chat: "What's the weather like tomorrow?"
                    Task: Analyze the content of the question and return the most suitable case number.
                    Answer: 1
                    
                    Example 2:
                    User Chat: "I have a meeting with Dr. Lee next Monday at 10 AM."
                    Task: Analyze the content of the question and return the most suitable case number.
                    Answer: 2
                    
                    Example 3:
                    User Chat: "Did I have any appointments on the last Friday?"
                    Task: Analyze the content of the question and return the most suitable case number.
                    Answer: 3
                    
                    Example 4:
                    Task: Analyze the content of the question and return the most suitable case number.
                    User Chat: {question}
                    Answer:
                    """
    case1_template = """
            {persona}
            YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
            User input: {question}
            """
    case2_template = """
            {persona}
            The user's input contains information about a new event they want to add to their schedule. You have two tasks to perform:

            1. Respond kindly to the user's input. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
            2. Organize the event the user wants to add into a json format for saving in a database. The returned json will have keys for info, location, person, and date.
            - info: Summarizes what the user wants to do. This value must always be present.
            - location: If the user's event information includes a place, save that place as the value.
            - person: If th e user's event mentions a person they want to include, save that person as the value.
            - date: If the user's event information includes a specific date and time, save that date and time in datetime format. Dates should be organized based on the current time at the user's location. Current time is {current_time}.
            Separate the outputs for tasks 1 and 2 with a special token <separate>.

            Example for one-shot learning:

            User input: I have a meeting with Dr. Smith at her office on March 3rd at 10am.

            Response to user:
            Shall I add your meeting with Dr. Smith at her office on March 3rd at 10am to your schedule?
            <separate>
            {{
            "info": "meeting with Dr. Smith",
            "location": "Dr. Smith's office",
            "person": "Dr. Smith",
            "date": "2023-03-03T10:00:00"
            }}
            
            User input: {question}
            
            Response to user:
            """

    case3_template = """
    {persona}
    When responding to user inputs, it's crucial to adapt your responses to the specified output language, maintaining a consistent and accessible communication style. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT. Your responses should not only be accurate but also display empathy and understanding of the user's needs.
    You are equipped with a state-of-the-art RAG (Retrieval-Augmented Generation) technique, enabling you to dynamically pull relevant schedule information from a comprehensive database tailored to the user's specific inquiries. This technique enhances your ability to provide precise, context-aware responses by leveraging real-time data retrieval combined with advanced natural language understanding.
    
    Example:
    User Input: "What meetings do I have tomorrow?"
    RAG Retrieval: [project status update at 10 AM, client discussion at 3 PM]
    Response: Good morning! You have two meetings scheduled for tomorrow: the project status update at 10 AM and the client discussion at 3 PM. Would you like reminders for these, or is there anything else I can assist you with?
    
    Now respond to following User input, based on RAG Retrieval.
    User input: {question},
    RAG Retrieval: {schedule}
    Response:
    """