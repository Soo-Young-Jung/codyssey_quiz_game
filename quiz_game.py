from datetime import datetime
import json
import subprocess
import platform
import time

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
        self.save_score_historys = []

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

        user_answer = get_number_input("Enter your answer (1-5): ", 1, 5)

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
        self.score = 0  # 게임 시작 시 점수를 초기화한다.
        total_quiz_count = len(self.quizzes) # 총 퀴즈 개수를 계산한다.
        correct_quiz_count = 0  # 정답 개수를 초기화한다.
        
        for number, quizz in enumerate(self.quizzes, start=1):


            # 콘솔 화면을 지운다.
            clear_console()

            print("# 5번 선택시 힌트를 확인할 수 있습니다(사용시 5점 차감).")
            print("# 6번 선택시 게임을 메뉴로 돌아갑니다.")

            print(f"\n{number} 번 퀴즈 :")
            quizz.show_question()
            user_answer = get_number_input("정답을 입력하세요 (1~4) : ", 1, 6)

            if(user_answer == 6):
                print("메뉴로 돌아갑니다.")
                self.go_back_to_menu()
                return
            elif(user_answer == 5):
                print(f"힌트: {quizz.hint}")
                self.score -= 5
                user_answer = get_number_input("정답을 입력하세요 (1~4) : ", 1, 6)

                while True:
                    if(user_answer == 6):
                        print("메뉴로 돌아갑니다.")
                        self.go_back_to_menu()
                        return
                    elif(user_answer == 5):
                        print("힌트는 이미 확인하셨습니다. 다시 정답을 입력하세요.")
                        user_answer = get_number_input("정답을 입력하세요 (1~4) : ", 1, 6)
                        continue
                    else:
                        if quizz.check_answer(user_answer):
                            print("정답입니다!")
                            self.score += 20
                            correct_quiz_count += 1
                        else:
                            print(f"오답입니다! 정답은 {quizz.answer}입니다.")
                        break

            else:
                if quizz.check_answer(user_answer):
                    print("정답입니다!")
                    self.score += 20
                    correct_quiz_count += 1
                else:
                    print(f"오답입니다! 정답은 {quizz.answer}입니다.")


        # 힌트 사용으로 인해 점수가 0점 미만이 되는 경우를 처리한다.
        if(self.score < 0):
            self.score = 0

        # 게임 기록 생성
        score_history = {
            "score": self.score,
            "date": int(time.time()),
            "correct_quiz_count": correct_quiz_count,
            "total_quiz_count": total_quiz_count
        }

        # 게임 기록 리스트에 추가
        self.save_score_historys.append(score_history)

        # 콘솔 화면을 지운다.
        clear_console()

        print(f"\n게임 종료! 최종 점수: {self.score}점")
        print(f"정답 개수: {correct_quiz_count}/{total_quiz_count}")

        # 최고 점수 갱신 및 출력
        if(self.score > self.best_score):
            self.best_score = self.score
            print(f"축하합니다! 새로운 최고 점수: {self.best_score}점")

        self.save_data()
        self.go_back_to_menu()


    def add_quiz(self):
        """ 
        새로운 퀴즈를 추가하는 메서드
        """

        question = get_text_input("퀴즈를 입력하세요 : ")
        choices = []
        for i in range(4):
            choice = get_text_input(f"{i + 1}번 선택지를 입력하세요 : ")
            choices.append(choice)

        answer = get_number_input("정답 번호를 입력하세요 (1~4) : ", 1, 4)
        hint = get_text_input("힌트를 입력하세요 : ")

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)

        self.save_data()
        self.go_back_to_menu()


    def list_quizzes(self):
        """ 
        퀴즈 목록을 출력하는 메서드
        저장된 퀴즈 목록을 확인할 수 있다.
        퀴즈가 없는 경우를 처리한다.
        """

        clear_console()

        for number, quizz in enumerate(self.quizzes, start=1):
            print(f"\n{number} 번 퀴즈 :")
            print(f"퀴즈: {quizz.question}")

        self.go_back_to_menu()


    def show_score(self):
        """ 
        현재 점수를 출력하는 메서드
        최고 점수를 확인할 수 있다.
        퀴즈를 풀 때마다 최고 점수와 비교하고 갱신한다.
        최고 점수를 파일에 저장한다.
        아직 퀴즈를 풀지 않은 경우를 처리한다.
        """

        clear_console()

        print(f"현재 점수: {self.score}점 / 최고 점수: {self.best_score}점")
        print("=== 점수 기록 ===")
        for i, score_history in enumerate(self.save_score_historys, start=1):
            print(f"{i}. 점수: {score_history['score']}점, 날짜: {datetime.fromtimestamp(score_history['date']).strftime('%Y-%m-%d %H:%M:%S')}, 정답을 맞춘 개수: {score_history['correct_quiz_count']}, 전체 퀴즈 수: {score_history['total_quiz_count']}")

        self.go_back_to_menu()


    def save_data(self):
        """ 
        퀴즈 데이터를 JSON 파일에 저장하는 메서드
        퀴즈 데이터와 최고 점수를 프로젝트 루트의 state.json 에 저장하는 기능을 구현한다.(UTF-8 인코딩 권장)
        JSON 파일에서 데이터를 불러오는 기능을 구현한다.
        파일이 없는 경우(첫 실행) 기본 퀴즈 데이터를 사용한다.
        파일이 손상되었거나 읽기/쓰기 오류가 발생한 경우를 try/except 로 처리한다.
        최소 스키마 예시(데이터 형태 참고; 키 이름/구조는 일관되게 유지):
        quizzes: 퀴즈 목록
        best_score: 최고 점수(또는 최고 정답 수 등)
        save_score_historys: 점수 기록 목록
        """

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
            "best_score": self.best_score,
            "save_score_historys": [
                {
                    "score": save_score_history["score"],
                    "date": save_score_history["date"],
                    "correct_quiz_count": save_score_history["correct_quiz_count"],
                    "total_quiz_count": save_score_history["total_quiz_count"]
                }
                for save_score_history in self.save_score_historys
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
        save_score_historys: 점수 기록 목록
        """

        try:
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
                    self.save_score_historys = data.get("save_score_historys", []);

        except FileNotFoundError:
            print("데이터 파일이 없습니다. 기본 데이터를 사용합니다.")
            self.reset_quizzes()

        except json.JSONDecodeError:
            print("데이터 파일이 손상되었습니다. 기본 데이터를 사용합니다.")
            self.reset_quizzes()

        except OSError as error:
            print(f"데이터 파일을 읽을 수 없습니다: {error}")
            self.reset_quizzes()



    def go_back_to_menu(self):
        """ 
        메뉴로 돌아가는 메서드
        유저가 특정 키를 입력해야만 메뉴로 돌아가도록 안내한다.
        """
        input("메뉴로 돌아가려면 Enter 키를 누르세요...")
        self.show_menu()

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
                "다음 중 파이썬에서 변수에 값을 저장하는 올바른 방법은 무엇인가요?",
                ["number := 10;", "number = 10", "10 = number", "int number = 10"],
                2,
                "변수에 값을 대입할 때 사용하는 기호를 생각해 보세요."
            ),

            Quiz(
                "다음 코드의 실행 결과로 올바른 것은 무엇인가요? print(type(\"Hello\"))",
                ["<class 'float'>", "<class 'bool'>", "<class 'int'>", "<class 'str'>"],
                4,
                "문자열의 타입을 확인하세요."
            ),

            Quiz(
                "다음 코드에서 출력되는 값은 무엇인가요? score = 75 if score >= 80: print(\"합격\") else: print(\"불합격\")",
                ["아무것도 출력되지 않음", "합격", "불합격", "75"],
                3,
                "조건문의 결과에 따라 다른 값을 출력합니다."
            ),

            Quiz(
                "다음 코드가 실행되었을 때 출력되는 값은 무엇인가요? for i in range(3): print(i)",
                ["0, 1, 2", "1, 2, 3", "0, 1, 2, 3", "0, 1, 2, 3, 4"],
                1,
                "range() 함수는 시작값부터 끝값 전까지의 숫자를 생성합니다."
            ),

            Quiz(
                "다음 함수의 실행 결과는 무엇인가요? def add(a, b): return a + b print(add(3, 5))",
                ["8", "15", "3", "5"],
                1,
                "return 문에서 수행하는 연산을 확인해 보세요."
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

def get_number_input(message, min_value, max_value):
    """
    사용자로부터 숫자 입력을 받고 범위를 벗어나면 다시 입력을 요청하는 함수
    값이 정상적인 경우에만 반환한다.
    """
    while True:
        user_input = input(message).strip()

        if not user_input:
            print("입력값이 비어 있습니다. 다시 입력하세요.")
            continue

        try:
            number = int(user_input)
        except ValueError:
            print("숫자만 입력할 수 있습니다.")
            continue

        if number < min_value or number > max_value:
            print(f"{min_value}~{max_value} 사이의 숫자를 입력하세요.")
            continue

        return number

def get_text_input(message):
    """
    사용자로부터 텍스트 입력을 받고 빈 문자열이 입력되면 다시 입력을 요청하는 함수
    값이 정상적인 경우에만 반환한다.
    """
    while True:
        user_input = input(message).strip()

        if not user_input:
            print("빈 문자열은 입력할 수 없습니다.")
            continue

        return user_input

def main():
    quiz_game = QuizGame()

    try:
        quiz_game.show_menu()

    except KeyboardInterrupt:
        print("\n사용자 요청으로 프로그램을 종료합니다.")

    except EOFError:
        print("\n입력이 종료되어 프로그램을 종료합니다.")

    finally:
        quiz_game.save_data()


if __name__ == "__main__":
    main()