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
                    5. The user's schedule may not exist, and if so, do not randomly create the user's schedule and only recommend activities that helps the user.
                    
                    Example:
                    User schedule: [Practice guitar, Calculate accuracy, Study backend development, Run AI models in the lab, Study NEXT.JS]
                    AI Recommendation: ["Jazz improvisation", "Statistical analysis project", "React coding challenge"]
                    
                    User schedule: {schedule}
                    AI Recommendation:
                    
    """

    recommendation_list_template = """
            Task: Generate comments for each schedule
            {persona}

            You will receive a list of the user's schedule information. Your task is to understand each schedule and generate a comment for each. There are a few rules you must follow in your comments:
            1. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
            2. Each comment should be concise, relevant to the schedule details, and realistic.
            3. Comments should be in sentence form, suitable for displaying alongside the schedule.
            4. Return the comments in a list format, without any additional commentary.
            
            Example:
            User schedule: 
            Start Time: 2024-05-25T18:00:00, Category: 공부 (ID: 1, Color: #0000FF), Person: 민주, Location: (Location not specified), Info: NEST.JS 공부하기
            Start Time: 2024-05-25T20:00:00, Category: 약속 (ID: 2, Color: #008000), Person: (Person not specified), Location: (Location not specified), Info: 개발 공모전 미팅하기
            Start Time: 2024-05-26T18:00:00, Category: 여가 (ID: 3, Color: #FF0000), Person: 채원, Location: 한강, Info: 친구랑 한강 놀러가기

            AI Comments: ["민주님과 어디에서 만나지는 정하셨나요? 장소가 정해지지 않았어요.", "오늘의 날씨는 확인하셨나요? 친구와 즐겁게 피크닉을 즐기세요!", "오늘의 날씨는 확인하셨나요? 친구와 즐겁게 피크닉을 즐기세요!"]
            
            User schedule: {schedule_list}
            AI Comments:
    """

    # case 분류 잘 안됨 - 수정 필요
    case_classify_template = """
                    Task: User Chat Classification
                    You are a case classifier integrated in scheduler application.
                    Please analyze User Chat according to the following criteria and return the appropriate case number (1, 2, 3).
                    {chat_type}
                
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

    chat_type_stt_template = """
            You should keep in mind that this user's input was written using speech to text technology.
            Therefore, there may be inaccuracies in the text due to errors in the STT process.
            You need to consider this aspect when performing the given task.
    """

    chat_type_user_template = """
    """

    case1_template = """
            {persona}
            {chat_type}
            YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT. Current time is {current_time}. Respond to the user considering the current time.
            User input: {question}
            """

    case2_template = """
            {persona}
            {chat_type}
            The user's input contains information about a new event they want to add to their schedule. You have two tasks to perform:
        
            1. Respond kindly to the user's input. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
            2. Organize the event the user wants to add into a json format for saving in a database. The returned json will have keys for info, location, person, start_time, end_time, and category. The category should include the name, id, and color.
            - info: Summarizes what the user wants to do. This value must always be present.
            - location: If the user's event information includes a place, save that place as the value.
            - person: If the user's event mentions a person they want to include, save that person as the value.
            - start_time: If the user's event information includes a specific date and time, save that date and time in datetime format. Dates should be organized based on the current time at the user's location. Current time is {current_time}.
            - end_time: If the user's event information includes an end time, save that date and time in datetime format.
            - category: Choose the most appropriate category for the event from the following list: {categories}. The category should include the name, id, and color.
            Separate the outputs for tasks 1 and 2 with a special token <separate>.
        
            Example for one-shot learning:
        
            User input: I have a meeting with Dr. Smith at her office on March 3rd from 10am to 11am.
        
            Response to user:
            Shall I add your meeting with Dr. Smith at her office on March 3rd from 10am to 11am to your schedule?
            <separate>
            {{
            "info": "meeting with Dr. Smith",
            "location": "Dr. Smith's office",
            "person": "Dr. Smith",
            "start_time": "2023-03-03T10:00:00",
            "end_time": "2023-03-03T11:00:00",
            "category": {{
                "name": "Work",
                "id": 1,
                "color": "#FF0000"
            }}
            }}
        
            User input: {question}
        
            Response to user:
    """

    case3_template = """
    {persona}
    {chat_type}
    Current time is {current_time}. Respond to the user considering the current time.
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