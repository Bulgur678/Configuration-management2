@echo off
chcp 65001

echo Первый тест
echo Простой граф
echo python main.py -p A -r "tests\test1.txt" -m test
python main.py -p A -r "tests\test1.txt" -m test
echo:

echo Второй тест
echo Граф с циклическими зависимостями
echo python main.py -p A -r "tests\test2.txt" -m test
python main.py -p A -r "tests\test2.txt" -m test
echo:

echo Третий тест
echo Сложный граф с множественными путями
echo python main.py -p A -r "tests\test3.txt" -m test
python main.py -p A -r "tests\test3.txt" -m test
echo:

echo Четвертый тест
echo Изолированные компоненты графа
echo python main.py -p A -r "tests\test4.txt" -m test
python main.py -p A -r "tests\test4.txt" -m test
echo:
echo:

pause