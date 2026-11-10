class Quiz:
    """ 
    Quiz 클래스
    개별 퀴즈를 표현하는 Quiz 클래스를 정의한다.
    속성: 문제(question), 선택지(choices), 정답(answer)
    선택지는 4개를 기본으로 한다.
    정답은 1~4 중 하나의 번호로 관리하는 방식을 권장한다. (구현에서 일관성 유지)
    메서드: 퀴즈 출력, 정답 확인 등 필요한 기능을 구현한다.
    """
    def __init__(self, question, choices, answer, hint):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def show_question(self):
        """ 
        퀴즈 문제와 선택지를 출력하는 메서드
        """
        print(self.question)

        """ 선택지를 출력 자료형식으로 출력한다. (1~4) """
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        """
        사용자가 입력한 답이 정답인지 확인하는 메서드
        """
        return self.answer == user_answer


""" 
기본 퀴즈 데이터
본인이 선택한 주제의 퀴즈 5개 이상을 직접 작성한다.
각 퀴즈는 문제, 선택지(4개), 정답을 포함한다.
Quiz 클래스의 인스턴스로 퀴즈를 생성한다.
"""
quizzes = [
    Quiz(
        "What is the capital of France?",
        ["Berlin", "Madrid", "Paris", "Rome"],
        3,
        "It's known as the city of love."
    ),

    Quiz(
        "What is the capital of Germany?",
        ["Paris", "Berlin", "Rome", "Madrid"],
        2,
        "It's the largest city in Germany."
    ),

    Quiz(
        "What is the capital of Italy?",
        ["Madrid", "London", "Rome", "Berlin"],
        3,
        "It's famous for the Colosseum."
    ),

    Quiz(
        "What is the capital of Spain?",
        ["Lisbon", "Madrid", "Paris", "Vienna"],
        2,
        "It's famous for the Prado Museum."
    ),

    Quiz(
        "What is the capital of Japan?",
        ["Osaka", "Kyoto", "Tokyo", "Nagoya"],
        3,
        "It's one of the world's largest metropolitan areas."
    )
]
