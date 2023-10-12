from connect import dbname, client_mongo, cache
from models import Author, Quote


exec(f"db = client_mongo.{dbname}")


@cache
def search_in_db(authors, quotes, name=None, tag=None):
    result = []
    if name:
        filtered_authors = authors(fullname__iregex=name)
        filtered_quotes = quotes(author__in=filtered_authors)
    elif tag:
        filtered_quotes = quotes(tags__iregex=tag)
    for quote in filtered_quotes:
        result.append(f"{quote.author.fullname}: {quote.quote}")
    return result


if __name__ == "__main__":
    authors = Author.objects
    quotes = Quote.objects
    while True:
        user_input = input(
            "Enter command in format '{exit|{name|tag|tags}: <value1>[,<value2>...]}': "
        )
        user_input = user_input.strip().casefold()
        if user_input == "exit":
            exit(0)
        print("")
        user_input = user_input.split(":")
        if len(user_input) != 2:
            continue
        command = user_input[0].strip()
        args = user_input[1].strip()
        result = set()
        match command:
            case "name":
                searched = search_in_db(authors, quotes, name=args)
                if searched:
                    for item in searched:
                        result.add(item)
            case "tag":
                searched = search_in_db(authors, quotes, tag=args)
                if searched:
                    for item in searched:
                        result.add(item)
            case "tags":
                args = args.split(",")
                for arg in args:
                    searched = search_in_db(authors, quotes, tag=arg.strip())
                    if searched:
                        for item in searched:
                            result.add(item)
            case _:
                continue
        for quote in result:
            print(quote, "\n")
