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
            2. Each comment should be concise, relevant to the schedule details, and realistic. You are able to give advice to the user, if needed.
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

    case_classify_template = """
                    Task: User Chat Classification
                    You are a case classifier integrated in scheduler application.
                    Please analyze User Chat according to the following criteria and return the appropriate case number (1, 2, 3, 4).
                    {chat_type}
                
                    - Case 1: \
                    The question is a general information request, advice, or simple conversation, and does not require accessing the user's schedule database.
                    - Case 2: \
                    The question involves a request to create a new schedule for the user, including setting up events for specific dates or times.
                    - Case 3: \
                    The question requires accessing or searching through the user's previous schedule information. This might involve past schedules, preferences, or other relevant details.
                    - Case 4: \
                    The question involves a request to delete an event or events from the user's schedule, necessitating identification and removal of specific entries from the database.
                    
                    After analyzing the content of the question, return the most suitable case number.
                    YOU MUST ANSWER ONLY WITH NUMBER (1, 2, 3, 4). OTHER WORDS ARE PROHIBITED. IT IS VERY IMPORTANT TO RETURN ONLY THE NUMBERS. NO YAPPING!
                    
                    Task: Analyze the content of the question and return the most suitable case number.
                    Example 1:
                    User Chat: "What's the weather like tomorrow?"
                    Answer: 1
                    
                    Example 2:
                    User Chat: "I have a meeting with Dr. Lee next Monday at 10 AM."
                    Answer: 2
                    
                    Example 3:
                    User Chat: "Did I have any appointments on the last Friday?"
                    Answer: 3

                    Example 4:
                    User Chat: "Please delete my appointment with Dr. Smith next Tuesday."
                    Answer: 4
                    
                    Example 5:
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
            The user's input contains information about several new events they want to add to their schedule. You have two tasks to perform:
            
            1. Respond kindly to the user's input. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
            2. Organize the events the user wants to add into a json format for saving in a database. Each event should be represented as a separate json object within a list. Each json object will have keys for info, location, person, start_time, end_time, and category. The category should include the name, id, and color. 
            - info: Summarizes what the user wants to do. This value must always be present.
            - location: If the user's event information includes a place, save that place as the value.
            - person: If the user's event mentions a person they want to include, save that person as the value.
            - start_time: If the user's event information includes a specific date and time, save that date and time in ISO 8601 datetime format. Dates should be organized based on the current time. Current time is {current_time}.
            - end_time: If the user's event information includes an end time, save that date and time in ISO 8601 datetime format.
            - category: Choose the most appropriate category for the event from the following list: {categories}. The category should include the name, id, and color.
            Separate the outputs for tasks 1 and 2 with a special token <separate>. Even if there is only one JSON object, it must be enclosed within a list.
            
            Example for one-shot learning:
            
            User input: I have a meeting with Dr. Smith at her office on March 3rd from 10am to 11am, and a dinner with John at the Italian restaurant on March 4th at 7pm.
            
            Response to user:
            Shall I add your meeting with Dr. Smith at her office on March 3rd from 10am to 11am and your dinner with John at the Italian restaurant on March 4th at 7pm to your schedule?
            <separate>
            [
              {{
                "info": "meeting with Dr. Smith",
                "location": "Dr. Smith's office",
                "person": "Dr. Smith",
                "start_time": "2023-03-03T10:00:00+09:00",
                "end_time": "2023-03-03T11:00:00+09:00",
                "category": {{
                  "name": "Work",
                  "id": 1,
                  "color": "#FF0000"
                }}
              }},
              {{
                "info": "dinner with John",
                "location": "Italian restaurant",
                "person": "John",
                "start_time": "2023-03-04T19:00:00+09:00",
                "end_time": null,  // Assuming end time is not specified
                "category": {{
                  "name": "Personal",
                  "id": 2,
                  "color": "#00FF00"
                }}
              }}
            ]
            
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

    case4_template = """
    {persona}
    {chat_type}
    The user's input contains information about several events they want to delete in their schedule. You have two tasks to perform:
            
            1. Respond kindly to the user's input. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
            2. You will be given a list of potential candidates from the database for events that the user may want to delete, and you must organize those events that the user has indicated they want to delete into a list. Organize the events the user wants to delete into a json format to make a delete api call in a database. Each event should be represented as a separate json object within a list. Each json object will have keys for info, location, person, start_time, end_time, and category. The category should include the name, id, and color. 
            - id: Find the id of the schedule in the 'ids'.
            - info: The document data of the schedule.
            - location: Include the venue or place where the event was scheduled to occur.
            - person: List any specific individuals involved in the event.
            - start_time: The scheduled start time of the event in ISO 8601 datetime format.
            - end_time: The scheduled end time of the event in ISO 8601 datetime format.
            - category: The event category with name, id, and an optional color.

            Separate the outputs for tasks 1 and 2 with a special token <separate>. Even if there is only one JSON object, it must be enclosed within a list.
            
            Example for one-shot learning:
            
            User input: 개발 공부하기와 한강에서의 놀러가기 이벤트를 삭제해 주세요.
            
            Schedules: {{'ids': [['29', '8', '7', '25', '16']], 'distances': [[0.1681539537965312, 0.17174183647570107, 0.2014914961195574, 0.2014914961195574, 0.21989337760155114]], 'embeddings': None, 'metadatas': [[{{'category': '🍀미분류', 'category_id': 29, 'date': 27, 'datetime_end': '2024-05-27T16:00:00Z', 'datetime_start': '2024-05-27T15:00:00Z', 'location': '공대', 'member': 1, 'month': 5, 'person': '', 'year': 2024}}, {{'category': '공부', 'category_id': 8, 'date': 25, 'datetime_end': '2024-05-25T16:00:00Z', 'datetime_start': '2024-05-25T15:00:00Z', 'location': '카페', 'member': 1, 'month': 5, 'person': '민주, 채원', 'year': 2024}}, {{'category': '공부', 'category_id': 7, 'date': 10, 'datetime_end': '2024-05-10T00:00:00Z', 'datetime_start': '2024-05-10T00:00:00Z', 'location': '한강', 'member': 1, 'month': 5, 'person': '혜승', 'year': 2024}}, {{'category': '🍀미분류', 'category_id': 25, 'date': 10, 'datetime_end': '2024-05-10T00:00:00Z', 'datetime_start': '2024-05-10T00:00:00Z', 'location': '한강', 'member': 1, 'month': 5, 'person': '혜승', 'year': 2024}}, {{'category': '📖 공부', 'category_id': 16, 'date': 15, 'datetime_end': '2024-05-15T16:00:00Z', 'datetime_start': '2024-05-15T15:00:00Z', 'location': '', 'member': 3, 'month': 5, 'person': '', 'year': 2024}}]], 'documents': [['개발 공부하기', '열심히 개발하기', '한강 놀러가기', '한강 놀러가기', '리액트 공부하기']], 'uris': None, 'data': None}}

            Response to user:
            Shall I add your meeting with Dr. Smith at her office on March 3rd from 10am to 11am and your dinner with John at the Italian restaurant on March 4th at 7pm to your schedule?
            <separate>
            [
                {{
                    "id": 29
                    "info": "개발 공부하기",
                    "location": "공대",
                    "person": "",
                    "start_time": "2024-05-27T15:00:00Z",
                    "end_time": "2024-05-27T16:00:00Z",
                    "category": {{
                        "name": "🍀미분류",
                        "id": 29,
                        "color": ""
                    }}
                }},
                {{
                    "id": 7
                    "info": "한강 놀러가기",
                    "location": "한강",
                    "person": "혜승",
                    "start_time": "2024-05-10T00:00:00Z",
                    "end_time": "2024-05-10T00:00:00Z",
                    "category": {{
                        "name": "🍀미분류",
                        "id": 25,
                        "color": ""
                    }}
                }}
            ]

            User input: {question}
            
            Schedules: {schedule}
            
            Response to user:
    """