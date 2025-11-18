import urllib.request
import io
import gzip
from collections import deque
import copy
from warnings import deprecated


class APK_Dependency:

    def __init__(self, package_name: str, repo_url: str, repo_mode: str, transitive_off: bool):
        self.package_name = package_name
        self.repo_url = repo_url
        self.repo_mode = repo_mode
        self.apk_text = self.fetch_apkindex_text(repo_url)
        self.transitive_off = transitive_off


    def fetch_apkindex_text(self, repo_url: str) -> str:
        #test-mode
        if self.repo_mode == "test":
            with open(self.repo_url, "r", errors='ignore') as file:
                text = file.read()
                return text
        #remote-mode
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
        if package_name.strip().startswith("so:"):
            temp_D = ""

            for line in apkindex_text.splitlines():
                if line.startswith('D:'):
                    temp_D = line[2:].strip()

                if line.startswith('p:') and package_name in line:
                    return  temp_D
        else:
            in_block = False
            for line in apkindex_text.splitlines():
                if line.startswith('P:'):
                    if line[2:].strip() == package_name:
                        in_block = True
                    else:
                        in_block = False
                else:
                    if in_block and line.startswith("D:"):
                        return line[2:].strip()

    def clean_dependencies(self, dep_line: str):
        if not dep_line:
            return []

        dep_row = dep_line.split(" ")

        for i in range(len(dep_row)):
            if "=" in dep_row[i]:
                dep_row[i] = dep_row[i].split("=",1)[0]

        return dep_row

    def run(self, package_name):

        dep_line = self.find_package_dependence(self.apk_text, package_name)

        dependencies = self.clean_dependencies(dep_line)

        return dependencies


    def build_graph(self):
        self.graph = {}
        self.visited_bfs = set()

        # Инициализируем BFS очередь
        queue = deque([self.package_name])

        # Запускаем рекурсивный BFS
        self.BFS_r(queue)

        #Копируем граф без транзитивности
        self.graph_without_transitive = copy.deepcopy(self.graph)


        #Добавляем транзитивность
        for name, set_dep in self.graph.items():
            self.add_transitive_edges_iterative(name)

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
                if dep not in self.visited_bfs: #
                    queue.append(dep)
                    addable.append(dep)


            self.graph[current_package] = set(addable)
            self.visited_bfs.add(current_package)

        self.BFS_r(queue)

    def add_transitive_edges_iterative(self, start_package: str):
        """Итеративное добавление транзитивных зависимостей через BFS"""
        visited = set()
        queue = deque(self.graph[start_package])  # начинаем с прямых зависимостей

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            try:
                # Добавляем зависимости текущего пакета к исходному
                dependencies = self.run(current)
                for dep in dependencies:
                    if dep != start_package:  # избегаем петель
                        self.graph[start_package].add(dep)
                        if dep not in visited:
                            queue.append(dep)
            except Exception as e:
                print(f"Ошибка при обработке {current}: {e}")


    def print_graph(self):
        # Вложенная функция
        def clean_name(name):
            """Убирает so: и .so с номером версии из имени пакета"""
            # Убираем префикс so: если есть
            if name.startswith('so:'):
                name = name[3:]
            # Убираем .so и все что после
            if '.so' in name:
                name = name.split('.so')[0]
            return name

        if self.transitive_off:
            graph = self.graph_without_transitive
            print("\n--- Граф зависимостей (Без транзитивности) ---")
        else:
            graph = self.graph
            print("\n--- Граф зависимостей (с транзитивностью) ---")

        for package, deps in graph.items():
            clean_package = clean_name(package)
            clean_deps = [clean_name(dep) for dep in sorted(deps)]

            if clean_deps:
                print(f"{clean_package} -> {', '.join(clean_deps)} \n")
            else:
                print(f"{clean_package} -> (нет зависимостей)\n")
