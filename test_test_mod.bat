@echo off
chcp 65001

echo Первый тест
echo Простой граф
echo python main.py -p E -r "tests\test1.txt" -m test -R
python main.py -p E -r "tests\test1.txt" -m test -R
echo:


echo Второй тест
echo Сложный граф с множественными путями с транзитивностью
echo python main.py -p L -r "tests\test3.txt" -m test -R
python main.py -p L -r "tests\test3.txt" -m test -R
echo:


echo Третий тест
echo Сложный граф с множественными путями без транзитивности
echo python main.py -p L -r "tests\test3.txt" -m test -R -tf
python main.py -p L -r "tests\test3.txt" -m test -R -tf
echo:

echo Четвертый тест
echo Изолированные компоненты графа
echo python main.py -p B -r "tests\test4.txt" -m test -R
python main.py -p B -r "tests\test4.txt" -m test -R
echo:
echo:

pause