import urllib.request
import io
import gzip

class APK_Dependency:
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
            raise RuntimeError(f"Пакет '{package_name}' не найден в APKINDEX")
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
            if dep_row[i].startswith("so:"):
                dep_row[i] = dep_row[i][3:].split(".so",1)[0]

        return dep_row

    def run(self, package_name: str, repo_url: str):

        apkindex_text = self.fetch_apkindex_text(repo_url)
        block_lines = self.find_package_block(apkindex_text, package_name)
        dep_line = self.extract_dep_line(block_lines)
        dependencies = self.clean_dependencies(dep_line)


        print(f"Прямые зависимости пакета '{package_name}':")
        if dependencies:
            for dep in dependencies:
                print(f"- {dep}")
            print()
        else:
            print("Зависимости не найдены или пакет не имеет прямых зависимостей.")

