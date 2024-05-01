class Template:
    daily_email_template = """
                    You will receive a day's worth of the user's schedule information. Your task is to understand that schedule and, based on it, recommend an activity for the user to perform that day. There are a few rules you must follow in your recommendations:
                    1. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
                    
                    Example:
                    User schedule:  [Practice guitar, Calculate accuracy, Study backend development, Run AI models in the lab, Study NEST.JS]
                    AI email: "공부 사이에 짧게 산책 어때요?"
                    
                    User schedule: {schedule}
                    AI email:
                    """