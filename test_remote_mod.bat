@echo off
chcp 65001

echo Первый тест
echo python main.py -p zsh -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/ -R
python main.py -p zsh -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/
echo:

echo ======================================================================================================
echo Второй тест
echo python main.py -p zsh -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/ -R -tf
python main.py -p zsh -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/ -R -tf

echo:
echo:

pause