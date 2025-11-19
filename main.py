import argparse
from CLI_APK import APK_Dependency

def command_line():
    args = {}
    parser = argparse.ArgumentParser (
        description='CLI'
    )

    #Имя пакета
    parser.add_argument( "-p", '--package-name',
                        type=str,
                        help="Введите имя пакета",
                        required=True)
    # URL репозитория
    parser.add_argument('-r', '--repo-url',
                        type=str,
                        help='URL-адрес репозитория или путь к файлу тестового репозитория',
                        required=True)

    # Режим работы с репозиторием
    parser.add_argument( '-m', '--repo-mode',
                        type=str,
                        choices=['remote', 'test'],
                        default='remote',
                        help='Режим работы с тестовым репозиторием (remote, test)')

    # Имя файла для изображения
    parser.add_argument('-o', '--output-image',
                        help='Имя сгенерированного файла с изображением графа')

    # Режим Транзитивности
    parser.add_argument('-tf', '--transitive_off',
                        action='store_true',
                        help='Режим вывода зависимостей в без транзитивности')

    # Режим Транзитивности
    parser.add_argument('-R', '--reverse',
                        action='store_true',
                        help='Режим вывода обратных зависимостей')

    # Режим ASCII-дерева
    parser.add_argument('-a', '--ascii-tree',
                        action='store_true',
                        help='Режим вывода зависимостей в формате ASCII-дерева')

    args = parser.parse_args()  #Парсинг аргументов

    args_dict = vars(args)

    return args_dict

    #package_name: name
    #repo_url: \some\url
    #repo_mode: test
    #output_image: None
    #transitive_off: False
    #reverse: False
    #ascii_tree: False

args_dict = command_line()

#объект класса
apk_dep = APK_Dependency(args_dict["package_name"], args_dict["repo_url"],
                         args_dict["repo_mode"], args_dict["transitive_off"],
                         args_dict["reverse"])

# Вызов метода
apk_dep.build_graph()


apk_dep.print_graph()






