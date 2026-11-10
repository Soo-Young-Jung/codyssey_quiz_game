class Quiz:
    """ 
    Quiz 클래스
    개별 퀴즈를 표현하는 Quiz 클래스를 정의한다.
    속성: 문제(question), 선택지(choices), 정답(answer)
    선택지는 4개를 기본으로 한다.
    정답은 1~4 중 하나의 번호로 관리하는 방식을 권장한다. (구현에서 일관성 유지)
    메서드: 퀴즈 출력, 정답 확인 등 필요한 기능을 구현한다.
    Git: Quiz 클래스 작성 후 커밋한다.
    """
    def __init__(self):
        self.question = None
        self.choices = []
        self.answer = None

        

