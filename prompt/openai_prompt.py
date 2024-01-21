class Template:
    case_template = "User Question Analysis and Classification: {question}" \
                    "Please analyze this question according to the following criteria and return the appropriate case number (1, 2, 3)." \
                    "- Case 1: The question is a general information request, advice, or simple conversation, and does not require accessing or creating the user's schedule database." \
                    "- Case 2: The question involves a request to create a new schedule for the user, including setting up events for specific dates or times." \
                    "- Case 3: The question requires accessing or searching through the user's previous schedule information. This might involve past schedules, preferences, or other relevant details." \
                    "After analyzing the content of the question, return the most suitable case number." \
                    "Answer only with number (1, 2, 3)."