import argparse

def command_line():
    args = {}
    parser = argparse.ArgumentParser (
        description='CLI'
    )

    #Имя пакета
    parser.add_argument( "-p", '--package-name',
                        type=str,
                        help="Введите ваше имя",
                        required=True)
    # URL репозитория
    parser.add_argument('-r', '--repo-url',
                        type=str,
                        default='',
                        help='URL-адрес репозитория или путь к файлу тестового репозитория')

    # Режим работы с репозиторием
    parser.add_argument( '-m', '--repo-mode',
                        type=str,
                        choices=['local', 'remote', 'test'],
                        default='local',
                        help='Режим работы с тестовым репозиторием (local, remote, test)')

    # Имя файла для изображения
    parser.add_argument('-o', '--output-image',
                        type=str,
                        help='Имя сгенерированного файла с изображением графа')

    # Режим ASCII-дерева
    parser.add_argument('-a', '--ascii-tree',
                        action='store_true',
                        help='Режим вывода зависимостей в формате ASCII-дерева')

    args = parser.parse_args()  #Парсинг аргументов

    args_dict = vars(args)

    print(50*"=")
    for key, value in args_dict.items():
        print(f"{key}: {value}")


command_line()
