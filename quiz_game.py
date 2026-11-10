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

class QuizGame:
    """ 
    게임 전체를 관리하는 QuizGame 클래스를 정의한다.
    속성: 퀴즈 목록, 최고 점수 등
    메서드: 메뉴 표시, 퀴즈 풀기, 퀴즈 추가, 목록 보기, 점수 확인, 파일 저장/불러오기 등
    """
    def __init__(self, quizzes):
        self.quizzes = quizzes
        self.best_score = 0

    def show_menu(self):
        """ 
         메뉴 표시하는 메서드
        """

    def play(self):
        """ 
        게임을 시작하는 메서드
        저장된 퀴즈를 출제한다.
        사용자가 정답을 입력할 수 있다.
        정답/오답 여부를 알려준다.
        모든 문제를 풀면 결과를 표시한다.
        퀴즈가 없는 경우를 처리한다.
        """

    def add_quiz(self):
        """ 
        새로운 퀴즈를 추가하는 메서드
        """


    def list_quizzes(self):
        """ 
        퀴즈 목록을 출력하는 메서드
        저장된 퀴즈 목록을 확인할 수 있다.
        퀴즈가 없는 경우를 처리한다.
        """


    def show_score(self):
        """ 
        현재 점수를 출력하는 메서드
        최고 점수를 확인할 수 있다.
        퀴즈를 풀 때마다 최고 점수와 비교하고 갱신한다.
        최고 점수를 파일에 저장한다.
        아직 퀴즈를 풀지 않은 경우를 처리한다.
        """


    def save_data(self):
        """ 
        퀴즈 데이터를 JSON 파일에 저장하는 함수
        퀴즈 데이터와 최고 점수를 프로젝트 루트의 state.json 에 저장하는 기능을 구현한다.(UTF-8 인코딩 권장)
        JSON 파일에서 데이터를 불러오는 기능을 구현한다.
        파일이 없는 경우(첫 실행) 기본 퀴즈 데이터를 사용한다.
        파일이 손상되었거나 읽기/쓰기 오류가 발생한 경우를 try/except 로 처리한다.
        최소 스키마 예시(데이터 형태 참고; 키 이름/구조는 일관되게 유지):
        quizzes: 퀴즈 목록
        best_score: 최고 점수(또는 최고 정답 수 등)
        """


    def load_data(self):
        """ 
        JSON 파일에서 퀴즈 데이터를 불러오는 함수
        """
    


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
