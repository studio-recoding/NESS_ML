class Template:
    daily_email_template = """
                    Construct an email to conclude the user's day. The email should:
                    
                    Acknowledge the user's efforts and achievements throughout the day.
                    Express gratitude for their hard work.
                    Offer encouragement and suggestions for preparing for tomorrow’s agenda.
                    Use this information to create a personalized, thoughtful email that reinforces positive feedback and provides motivational insights for the upcoming day.
                    YOU MUST USE {output_language} TO RESPOND.
                    
                    Today's schedule for the user:
                    2021-07-19T09:00:00: 줌 회의 참석
                    2021-07-19T11:00:00: 프로젝트 보고서 검토
                    2021-07-19T13:00:00: 비즈니스 점심 식사
                    2021-07-19T15:00:00: 팀 미팅
                    2021-07-19T18:00:00: 워크샵 준비
                    
                    Email:
                    오늘 하루 동안의 일정을 보면 많은 일을 처리하신 것으로 보입니다.

                    오전에는 중요한 줌 회의에 참석하셨습니다. 회의에 적극적으로 참여하신 점이 인상적이었습니다.
                    프로젝트 보고서를 검토하는 시간에는 세부 사항에 주의를 기울이셨습니다. 이런 세심함이 프로젝트의 성공에 크게 기여할 것입니다.
                    비즈니스 점심 식사는 관계 구축에 있어 중요한 시간이었습니다. 이러한 네트워킹은 앞으로의 업무에도 도움이 될 것입니다.
                    오후의 팀 미팅에서는 팀원들과의 소통을 잘 이끌어 나가셨습니다. 팀의 협력을 증진시키는 데 중요한 역할을 하셨어요.
                    마지막으로, 워크샵 준비에도 힘써 주셔서 감사합니다. 이런 준비가 내일의 워크샵을 원활하게 진행될 수 있게 할 것입니다.
                    
                    하루 동안의 노력에 감사드립니다. 휴식을 취하며 내일을 위한 에너지를 충전하시길 바랍니다. 내일도 좋은 하루 되세요!
                    
                    Today's schedule for the user:
                    {schedule} 
                    
                    Email:
                    """