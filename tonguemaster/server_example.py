from tonguemaster.server_if import ServerIf


def main():
    # TODO: don't forget to change the dir name:
    server_if = ServerIf(db_paths=[r'C:\Users\eldad\Documents\proj\pythonProject\server_p\DB_dir'])
    server_if.start_servers()

    word_list = [('neldad', 'Eldad'),
                 ('neload', 'Epdad'),
                 ('neljad', 'Elkad'),
                 ('nelmad', 'Eldvd'),
                 ('nelcad', 'Eldaq'),
                 ('qeldad', 'Eldtd'),
                 ('nelqad', 'Eldld'),
                 ('geldad', 'Elhad')]
    server_if.insert(word_list)

    print('fetch 5 words:')
    print('\t' + str(server_if.fetch_words(5)))
    updated_word_list = [('Eldad', 3.5, 0), ('Epdad', 1.5, -2)]
    server_if.update_words(updated_word_list)

    print("fetch 10 (after updating 2 words):")
    print('\t' + str(server_if.fetch_words(10)))
    print('fetch 6 dummy words:')
    print('\t' + str(server_if.fetch_dummy(6)))
    print('these word do\'nt exist in the dictionary:')
    exist_word = ['Eldad',
                  'Epdad',
                  'Elkad',
                  'Eldvd',
                  'Eldaq',
                  'Eldtd',
                  'Eldld',
                  'Eldvdd',
                  'Eldaqf',
                  'Eldtdg',
                  'Eldldh',
                  'Elhad']
    print('\t' + str(server_if.are_exist(exist_word)))

    server_if.stop_servers()


if __name__ == '__main__':
    main()
