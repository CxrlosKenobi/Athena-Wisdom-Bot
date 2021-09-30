def Clip():
    clippings = []
    with open('data/clippings.txt') as file:
        aux = 0
        unwanted = ['(', ')', '"']
        for line in file:
            if aux == 0:
                book, author = line, line
                aux += 1
            elif aux == 1:
                page, date = line, line
                aux += 1
            elif aux == 2:
                aux += 1
                continue
            elif aux == 3:
                highlight = line
                aux += 1
            elif aux == 4:
                out = {
                    'book': book,
                    'page': page,
                    'author': author,
                    'date': date,
                    'highlight': highlight   
                }
                clippings.append(out)
                aux = 0
    return clippings