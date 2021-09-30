highlight = input('> Highlight: ')
author = input("> Author: ")
book = input("> Book: ")

row_1 = f'\n{book} - {author}\n'
row_2 = f' | \n'
row_3 = f'\n'
row_4 = f'{highlight}\n'
row_5 = f'=========='

clipping = row_1 + row_2 + row_3 + row_4 + row_5
print(f'[ ! ] Are you sure you want to add this to your clippings?\n\033[92m{clipping}\033[0m')

if input("\n[ ! ] Type 'yes' to add: ") == 'yes':
    with open('../data/clippings.txt', 'a') as f:
        f.write(clipping)
    print('[ ok ] Clipping added!')
else:
    print('[ ok ] Cancelled.')
