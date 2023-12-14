BOOK: dict[int, str] = {}
DELIMITER_SYMBOLS: int = 1000
# Delimiter symbols: ", ", ". ", ": ", "; "
def book_in_dict() -> dict[int, str]:
    global BOOK
    with open("book\\book.txt", "r", encoding="utf-8") as file:
        data = [file.readline() for _ in file]
        data = [x.strip() for x in data if x != "\n"]
        pieces: list[list[str]] = []
        for row in data:
            pieces.append([])
            current = ""
            for i in range(len(row)):
                current += row[i]
                if row[i] in ",.;:!?":
                    pieces[-1].append(current)
                    current = ""
        pieces = [[x.strip() for x in row] for row in pieces]
        current = ""
        page = 1
        for piece in pieces:
            for i in range(len(piece)):
                BOOK[page] = "" if page not in BOOK else BOOK[page]
                if len(current) + len(piece[i]) + len(BOOK[page]) < DELIMITER_SYMBOLS:
                    current += piece[i]
                else:
                    BOOK[page] += current
                    current = ""
                    page += 1
        BOOK[page] = current
    return BOOK