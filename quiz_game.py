import json
import subprocess
import platform



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
    def __init__(self, quizzes=[]):
        self.quizzes = quizzes
        self.best_score = 0
        self.score = 0
        self.save_score_history = []

        # JSON 파일에서 데이터를 불러온다.
        self.load_data()

    def show_menu(self):
        """ 
         메뉴 표시하는 메서드
        """
        clear_console()
        
        print("=== Quiz Game ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 점수 확인")
        print("5. 종료")

        user_answer = int(input("Enter your answer (1-5): "))

        if user_answer == 1:
            self.play()
        elif user_answer == 2:
            self.add_quiz()
        elif user_answer == 3:
            self.list_quizzes()
        elif user_answer == 4:
            self.show_score()
        elif user_answer == 5:
            print("게임을 종료합니다.")
            exit()


    def play(self):
        """ 
        게임을 시작하는 메서드
        저장된 퀴즈를 출제한다.
        사용자가 정답을 입력할 수 있다.
        정답/오답 여부를 알려준다.
        모든 문제를 풀면 결과를 표시한다.
        퀴즈가 없는 경우를 처리한다.
        """
        
        for number, quizz in enumerate(self.quizzes, start=1):
            # 현재 플레이어의 점수를 초기화한다.
            self.score = 0

            print(f"\nQuestion {number}:")
            print("# 5번 선택시 힌트를 확인할 수 있습니다(사용시 5점 차감).")
            print("# 9번 선택시 게임을 메뉴로 돌아갑니다.")
            quizz.show_question()
            user_answer = int(input("정답을 입력하세요 : "))
            
            if quizz.check_answer(user_answer):
                print("정답입니다!")
                self.score += 20
            elif user_answer == 5:

                print(f"힌트: {quizz.hint}")
                self.score -= 5

                # 사용자가 힌트를 확인한 후 다시 답을 입력하도록 안내
                user_answer = int(input("정답을 입력하세요 : "))

                if quizz.check_answer(user_answer):
                    print("정답입니다!")
                    self.score += 20
                else:
                    print(f"오답입니다! 정답은 {quizz.answer}입니다.")

            else:
                print(f"오답입니다! 정답은 {quizz.answer}입니다.")

        # 최고 점수 갱신 및 출력
        if(self.score > self.best_score):
            self.best_score = self.score
            print(f"축하합니다! 새로운 최고 점수: {self.best_score}점")
            self.save_data()

        self.show_menu()


    def add_quiz(self):
        """ 
        새로운 퀴즈를 추가하는 메서드
        """

        question = input("퀴즈를 입력하세요 : ")
        choices = []
        for i in range(4):
            choice = input(f"{i + 1}번 선택지를 입력하세요 : ")
            choices.append(choice)

        answer = int(input("정답 번호를 입력하세요 (1-4) : "))
        hint = input("퀴즈에 대한 힌트를 입력하세요 : ")

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)

        self.save_data()
        self.show_menu()


    def list_quizzes(self):
        """ 
        퀴즈 목록을 출력하는 메서드
        저장된 퀴즈 목록을 확인할 수 있다.
        퀴즈가 없는 경우를 처리한다.
        """

        for number, quizz in enumerate(self.quizzes, start=1):
            print(f"\nQuestion {number} :")
            print(f"퀴즈: {quizz.question}")


    def show_score(self):
        """ 
        현재 점수를 출력하는 메서드
        최고 점수를 확인할 수 있다.
        퀴즈를 풀 때마다 최고 점수와 비교하고 갱신한다.
        최고 점수를 파일에 저장한다.
        아직 퀴즈를 풀지 않은 경우를 처리한다.
        """


    def save_data(self, save_data="score"):
        """ 
        퀴즈 데이터를 JSON 파일에 저장하는 메서드
        퀴즈 데이터와 최고 점수를 프로젝트 루트의 state.json 에 저장하는 기능을 구현한다.(UTF-8 인코딩 권장)
        JSON 파일에서 데이터를 불러오는 기능을 구현한다.
        파일이 없는 경우(첫 실행) 기본 퀴즈 데이터를 사용한다.
        파일이 손상되었거나 읽기/쓰기 오류가 발생한 경우를 try/except 로 처리한다.
        최소 스키마 예시(데이터 형태 참고; 키 이름/구조는 일관되게 유지):
        quizzes: 퀴즈 목록
        best_score: 최고 점수(또는 최고 정답 수 등)
        """

        if(save_data == "score"):
            data = {
                "quizzes": [
                    {
                        "question": quiz.question,
                        "choices": quiz.choices,
                        "answer": quiz.answer,
                        "hint": quiz.hint
                    }
                    for quiz in self.quizzes
                ],
                "best_score": self.best_score
            }

            try:
                with open("state.json", "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            except IOError:
                print("Error: Could not write to state.json")
        else:
            data = {
                "quizzes": [
                    {
                        "question": quiz.question,
                        "choices": quiz.choices,
                        "answer": quiz.answer,
                        "hint": quiz.hint
                    }
                    for quiz in self.quizzes
                ]
            }

            try:
                with open("state.json", "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            except IOError:
                print("Error: Could not write to state.json")



    def load_data(self):
        """ 
        JSON 파일에서 퀴즈 데이터를 불러오는 메서드
        파일이 손상되었거나 읽기/쓰기 오류가 발생한 경우를 try/except 로 처리한다.
        최소 스키마 예시(데이터 형태 참고; 키 이름/구조는 일관되게 유지):
        quizzes: 퀴즈 목록
        best_score: 최고 점수(또는 최고 정답 수 등)
        """
        with open("state.json", "r", encoding="utf-8") as file:
            data = json.load(file)

            # 퀴즈 데이터를 불러온다.
            quizzes = data.get("quizzes", [])

            # 퀴즈 데이터가 없는 경우 기본 퀴즈 데이터를 초기화한다.
            if(len(quizzes) == 0):
                self.reset_quizzes()
            else:
                # 퀴즈 데이터를 Quiz 클래스의 인스턴스로 변환하여 저장한다.
                self.quizzes = [
                    Quiz(
                        quiz_data["question"],
                        quiz_data["choices"],
                        quiz_data["answer"],
                        quiz_data["hint"]
                    )
                    for quiz_data in quizzes
                ]
                self.best_score = data.get("best_score", 0)


    def reset_quizzes(self):
        """ 
        퀴즈 데이터를 초기화하는 메서드
        기본 퀴즈 데이터 예시
        본인이 선택한 주제의 퀴즈 5개 이상을 직접 작성한다.
        각 퀴즈는 문제, 선택지(4개), 정답을 포함한다.
        Quiz 클래스의 인스턴스로 퀴즈를 생성한다.
        """
        self.quizzes = [
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

def clear_console():
    """ 
    콘솔 화면을 지우는 함수
    실행 환경이 윈도우일 때와 유닉스 계열일 때를 구분하여 처리한다.
    """
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"], shell=True)

quiz_game = QuizGame()

quiz_game.play()