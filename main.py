class Library:
    def __init__(self, idx: int, signup_time: int, shipping_rate: int, books: list):
        self.idx = idx
        self.signup_time = signup_time
        self.shipping_rate = shipping_rate
        self.books = books
        self.nbr_books = len(books)

    def select(self, scores: list, days: int, selected_books: list):
        days -= self.signup_time
        if days <= 0:
            return (0, [], 0)
        nbr_books = min(days * self.shipping_rate, self.nbr_books)
        books = []
        score = 0
        selected = 0
        for book in self.books:
            if selected_books[book] is False:
                books.append(book)
                score += scores[book]
                selected += 1
                if selected == nbr_books:
                    break
        return score, books, self.signup_time + selected / self.shipping_rate


def calculate_score(text, books):
    lines = text.split('\n')
    libraries_signed_up = int(lines.pop(0))
    scores = {}
    book_score = [False for _ in books]
    for idx in range(libraries_signed_up):
        values = list(map(int, filter(None, lines.pop(0).split(" "))))
        library_id = values[0]
        if library_id in scores.keys():
            raise Exception("Library not allowed multiple times")
        nbr_books = values[1]
        if nbr_books < 1:
            raise Exception("Do not list libraries with only one book")
        idx += 1
        values = list(map(int, filter(None, lines.pop(0).split(" "))))
        if len(values) != nbr_books:
            raise Exception("Wrong number of books setup, got {} expected {}"
                            .format(len(values), nbr_books))
        scores[library_id] = 0
        for book_id in values:
            if book_score[book_id] is False:
                scores[library_id] += books[book_id]
                book_score[book_id] = True
    sum = 0
    for score in scores.values():
        sum += score
    return sum

def read_file(path):
    with open(path) as text_file:
        # b=books, l = libraries, d = days
        b, l, d = list(map(int, text_file.readline().split(" ")))
        scores = list(map(int, text_file.readline().split(" ")))
        libraries = []
        for i in range(l):
            # n = books in library, t = signup days, m = delivery rate
            n, t, m = list(map(int, text_file.readline().split(" ")))
            books = sorted(
                list(set(map(int, text_file.readline().split(" ")))),
                key=lambda x: scores[x],
                reverse=True
            )
            libraries.append(Library(i, t, m, books))

    return scores, libraries, d

def write_file(path, result):
    with open(path, 'w') as out_file:
        out_file.write("{}\n".format(len(result)))
        for i, books in result:
            out_file.write("{} {}\n".format(i, len(books)))
            out_file.write(" ".join(map(str, books)))
            out_file.write("\n")
    with open(path) as submission:
        return submission.read()

def simple(scores, libraries, days):
    result = []
    scanned_books = [False for _ in scores]
    for i in range(len(libraries)):
        best_books = []
        best_score = 0
        best_lib = None
        for lib in libraries:
            score, books, total_days = lib.select(scores, days, scanned_books)
            score2, books2, total_days2 = lib.select(scores, days / 1.8, scanned_books)
            if score * 0.67 < score2:
                score = score2
                books = books2
                total_days = total_days2
            score = score / float(lib.signup_time)
            #score = score * float(total_days)
            if score > best_score:
                best_score = score
                best_books = books
                best_lib = lib
        if best_lib is None:
            break
        for book in best_books:
            scanned_books[book] = True
        libraries.remove(best_lib)
        days -= best_lib.signup_time
        print("\rdays: {}, signup: {}".format(days, best_lib.signup_time), end="")
        result.append((best_lib.idx, best_books))
    print("")
    return result

def main():
    paths = [
        #"a_example",
        #"b_read_on",
        "e_so_many_books",
        "f_libraries_of_the_world",
        #"c_incunabula",
        #"d_tough_choices",
    ]
    for path in paths:
        print(path)
        scores, libraries, d = read_file(path + ".txt")
        result = simple(scores, libraries, d)
        score = calculate_score(write_file(path + ".out", result), scores)
        print(score)

if __name__ == "__main__":
    main()
