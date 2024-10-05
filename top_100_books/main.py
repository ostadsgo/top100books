type NumberOrString = str | float | int
type Lines = list[str]
type Book = dict[str, NumberOrString]
type Books = list[Book]
type BookName = dict[str, str]


def readfile(filename: str) -> str:
    """Read file and return it's content."""
    with open(filename) as file:
        return file.read().strip()


def get_lines(content: str) -> Lines:
    """Get content as a string and split it with \n to get
    individuals lines."""
    return [line.strip() for line in content.split("\n")]


def goodreaders(lines: Lines) -> Books:
    """Pars data that grabed from goodreaders.com
    Extract book name, author, rank and rating
    """
    books = []
    start = 0
    for index in range(7, len(lines), 7):
        data = lines[start:index]
        book = {}
        book["number"] = int(data[0])
        book["name"] = data[1].split("\t")[0].title().strip()
        book["author"] = data[2].replace("by", "")
        book["rating"] = float(data[3].split()[0])
        book["ratings"] = int(data[3].split("—")[-1].split()[0].replace(",", ""))
        book["f_ratings"] = data[3].split("—")[-1].split()[0]
        books.append(book)
        start = index
    return books


def time_magazine(lines: Lines) -> list[BookName]:
    """Extract name of the books."""
    return [{"name": name.title().strip()} for name in lines]


def greatebooks_org(lines: Lines) -> Books:
    """Return books row, book name and author with summary"""
    start = 0
    books = []
    for end in range(4, len(lines), 4):
        book_data = lines[start: end]
        row = book_data[0].split("by")
        author_name = row[-1].strip()
        number, *book_name = row[0].split('.')
        book_name = "".join(book_name).strip()
        number = int(number)
        book = {"number": number, "name": book_name.title().strip(), "author": author_name} 
        books.append(book)
        start = end

    return books

def find_similer(*books: Books | list[BookName]) -> list[BookName]:
    """ Find similer books in all data collections. """
    similers = []
    gr = [book.get("name") for book in books[0]]
    ti = [book.get("name") for book in books[1]]
    gb = [book.get("name") for book in books[2]]
    for book in gr:
        if book in ti and book in gr:
            similers.append(book)
    #
    # for book in ti:
    #     if book in (gr + gb) and book not in similers:
    #         similers.append(book)
    #
    # for book in gb:
    #     if book in (gr + ti) and book not in similers:
    #         similers.append(book)
    return similers
    # return list(set(gr) & set(ti) & set(gb))


def main():
    # Goodreaders
    goodreaders_content = readfile("data/goodreaders.txt")
    goodreaders_lines = get_lines(goodreaders_content)
    goodreaders_data = goodreaders(goodreaders_lines)
    # Time Magazine
    time_mag = readfile("data/time.txt")
    time_mag_lines = get_lines(time_mag)
    time_mag_data = time_magazine(time_mag_lines)
    # Greatbooks.org
    gb_content = readfile("data/greatestbooks_org.txt")
    gb_lines = get_lines(gb_content)
    gb_data = greatebooks_org(gb_lines)

    similer_books = find_similer(goodreaders_data, time_mag_data, gb_data)
    for index, book in enumerate(similer_books):
        print(index, '. ', book)



if __name__ == "__main__":
    main()
