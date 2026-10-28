# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS, MAX_BOOKS = 14, 3


def _is_day(v):
    # bool 은 int 의 하위 클래스라 type 으로 정확히 비교해야 걸러짐
    return type(v) is int and v >= 1


class LibraryLoan:
    def __init__(self):
        self._loans = {}      # book_id → (name, 빌린 날)
        self._ban = {}        # name → 대출이 다시 가능한 첫 날

    def borrow(self, book_id, name, day):
        if not isinstance(name, str) or not name.strip():   # 빈 이름·공백·None 거절
            return False
        if book_id not in BOOKS:                              # 1. 없는 책 (튜플 비교라 리스트가 와도 예외 없음)
            return False
        if not _is_day(day):                                  # 2. 1 이상의 정수
            return False
        if book_id in self._loans:                            # 3. 이미 대출 중
            return False
        mine = [d for n, d in self._loans.values() if n == name]
        if len(mine) >= MAX_BOOKS:                            # 4. 3권 보유
            return False
        if any(day > d + LOAN_DAYS for d in mine):            # 5. 기한 지난 책 보유
            return False
        if day < self._ban.get(name, 0):                      # 6. 대출 정지
            return False
        self._loans[book_id] = (name, day)
        return True

    def return_book(self, book_id, name, day):
        if book_id not in BOOKS or not _is_day(day):
            return -1
        loan = self._loans.get(book_id)
        if loan is None or loan[0] != name or day < loan[1]:
            return -1
        del self._loans[book_id]
        late = max(0, day - (loan[1] + LOAN_DAYS))
        if late:
            # 반납한 날부터 late 일 동안 정지, 겹치면 더 늦게 끝나는 쪽
            self._ban[name] = max(self._ban.get(name, 0), day + late)
        return late

    def get_loans(self, name):
        # 반납 기한 순, 같으면 책 번호 순
        return sorted(((b, d + LOAN_DAYS) for b, (n, d) in self._loans.items() if n == name),
                      key=lambda t: (t[1], t[0]))
