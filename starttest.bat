@echo off
chcp 65001

echo Первый тест
echo python main.py -p abseil-cpp-cord-internal -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/ppc64le/

python main.py -p abseil-cpp-cord-internal -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/ppc64le/


echo Второй тест
echo python main.py -p nettle -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/

python main.py -p nettle -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/


echo Третий тест
echo python main.py -p abseil-cpp-leak-check -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64

python main.py -p abseil-cpp-leak-check -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64

echo:
pause