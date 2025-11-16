import urllib.request
import io
import gzip
from collections import deque
from warnings import deprecated


class APK_Dependency:

    def __init__(self, package_name, repo_url: str):
        self.package_name = package_name
        self.repo_url = repo_url
        self.apk_text = self.fetch_apkindex_text(repo_url)


    def fetch_apkindex_text(self, repo_url: str) -> str:

        repo_url = repo_url.rstrip('/')
        candidates = [
            f"{repo_url}/APKINDEX.tar.gz"#Если пользователь уже ввел архитектуру
        ]
        # общие архитектуры
        arches = ['x86_64', 'aarch64', 'armhf', 'armv7', 'ppc64le', 's390x']
        for arch in arches:
            candidates.append(f"{repo_url}/{arch}/APKINDEX.tar.gz")

        last_err = None
        for url in candidates:
            try:
                with urllib.request.urlopen(url) as resp:
                    data = resp.read()
                with gzip.GzipFile(fileobj=io.BytesIO(data)) as gz:
                    text = gz.read().decode('utf-8', errors='ignore')
                return text
            except Exception as e:
                last_err = e
                continue

        raise RuntimeError(f"Не удалось загрузить APKINDEX.tar.gz из репозитория. Последняя ошибка: {last_err}")

    def find_package_dependence(self, apkindex_text: str, package_name: str):
        if package_name.startswith("so:"):
            temp_P = ""
            for line in apkindex_text.splitlines():
                if line.startswith('P:'):
                    temp_P = line[2:].strip()

                if line.startswith('p:') and package_name in line:
                    return temp_P
        else:
            in_block = False
            for line in apkindex_text.splitlines():
                if line.startswith('P:'):
                    if line[2:].strip() == package_name:
                        in_block = True
                    else:
                        in_block = False
                else:
                    if in_block:
                        return line[2:].strip()

    def find_package_block(self, apkindex_text: str, package_name: str):

        in_block = False
        block_lines = []
        for line in apkindex_text.splitlines():
            if line.startswith('P:'):
                if line[2:].strip() == package_name:
                    in_block = True
                    block_lines = [line]
                else:
                    in_block = False
            else:
                if in_block:
                    block_lines.append(line)
                    if line.strip() == '':
                        break
        if not block_lines:
            #raise RuntimeError(f"Пакет '{package_name}' не найден в APKINDEX")
            block_lines = "D:NOT_FOUND_" + package_name
            print("ПРОВЕРКА = ", block_lines)
        return block_lines

    def extract_dep_line(self, block_lines):
        dep_line = None
        for line in block_lines:
            if line.startswith('D:'):
                dep_line = line[2:].strip()
                break
        return dep_line

    def clean_dependencies(self, dep_line: str):
        if not dep_line:
            return []

        dep_row = dep_line.split()
        for i in range(len(dep_row)):
            if "=" in dep_row[i]:
                dep_row[i] = dep_row[i].split("=",1)[0]

            # if "so:libz." in dep_row[i]:
            #     dep_row[i] = "libzmq"
            #
            # elif dep_row[i].startswith("so:libc.musl-"):
            #     dep_row[i] = "musl"

            elif dep_row[i].startswith("so:"):
                dep_row[i] = dep_row[i][3:].split(".so",1)[0]

        return dep_row

    def run(self, package_name):

        #block_lines = self.find_package_block(self.apk_text, package_name)
        #dep_line = self.extract_dep_line(block_lines)

        dep_line = self.find_package_dependence(self.apk_text, self.package_name)
        print("Без обработки = ", dep_line,"\n")
        dependencies = self.clean_dependencies(dep_line)

        return dependencies


    def build_graph(self):

        self.graph = {}
        self.visited_bfs = set()

        # Инициализируем BFS очередь
        queue = deque([self.package_name])

        # Запускаем рекурсивный BFS
        self.BFS_r(queue)

        # Добавляем транзитивные зависимости потом добавлю
        for name, set_dep in self.graph.items():
            temp_list = list(set_dep)
            for add in temp_list:
                self.add_transitive_edges(add, name)

        return self.graph

    def BFS_r(self, queue: deque ):
        if not queue:
            return
        # проход по всему уровню
        for _ in range(len(queue)):  # фиксируем длину на начало
            current_package = queue.popleft()
            dependencies = self.run(current_package)
            addable = []
            # добавляем сыновей
            for dep in dependencies:
                if dep not in self.visited_bfs:
                    queue.append(dep)
                    addable.append(dep)

            self.graph[current_package] = set(addable)
            self.visited_bfs.add(current_package)

        self.BFS_r(queue)


    def add_transitive_edges(self, current_package: str, add_to: str):
        dependencies = self.run(current_package)

        for dep in dependencies:
            self.add_transitive_edges(dep,add_to)

        self.graph[add_to].add(current_package)













