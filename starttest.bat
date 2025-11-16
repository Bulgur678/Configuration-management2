@echo off
chcp 65001

echo Первый тест
echo python main.py -p nrpe -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/
python main.py -p nrpe -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/
echo:

echo Второй тест
echo python main.py -p cvs-zsh-completion -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/
python main.py -p cvs-zsh-completion -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/
echo:

echo Третий тест
echo python python main.py -p nodejs-doc -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/
python main.py -p nodejs-doc -r https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/

echo:
echo:

pause