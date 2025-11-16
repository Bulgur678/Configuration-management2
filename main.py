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

    return args_dict

    #package_name: First_proggram
    #repo_url: \some\url
    #repo_mode: test
    #output_image: None
    #ascii_tree: False

args_dict = command_line()

#объект класса
apk_dep = APK_Dependency(args_dict["package_name"], args_dict["repo_url"])

# Вызов метода
print(apk_dep.run(args_dict["package_name"]),'\n')
#
#print(apk_dep.build_graph())

