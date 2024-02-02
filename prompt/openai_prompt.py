class Template:
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
                    YOU MUST ANSWER ONLY WITH NUMBER (1, 2, 3). OTHER WORDS ARE PROHIBITED. IT IS VERY IMPORTANT TO RETURN ONLY THE NUMBERS.
                    
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
    You are a friendly assistant who helps users manage their schedules. Respond kindly to the user's input. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
    User input: {question}
    """
    case2_template = """
        You are a friendly assistant who helps users manage their schedules. The user's input contains information about a new event they want to add to their schedule. You have two tasks to perform:

        1. Respond kindly to the user's input. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
        2. Organize the event the user wants to add into a json format for saving in a database. The returned json will have keys for info, location, person, and date.
        - info: Summarizes what the user wants to do. This value must always be present.
        - location: If the user's event information includes a place, save that place as the value.
        - person: If the user's event mentions a person they want to include, save that person as the value.
        - date: If the user's event information includes a specific date and time, save that date and time in datetime format.
        Separate the outputs for tasks 1 and 2 with a special token <separate>.

        Example for one-shot learning:

        User input: "I have a meeting with Dr. Smith at her office on March 3rd at 10am."

        Response to user:
        "I've added your meeting with Dr. Smith at her office on March 3rd at 10am to your schedule. Is there anything else you'd like to add or modify?"
        <separate>
        {{
            "info": "meeting with Dr. Smith",
            "location": "Dr. Smith's office",
            "person": "Dr. Smith",
            "date": "2023-03-03T10:00:00"
        }}

        User input: {question}
        """
    case3_template = """consider yourself as assistant who takes care of user's schedule,
    and answer the question refer to the user's schedule. Notice that you should answer in Korean.
    question: {question},
    schedule: {schedule}"""