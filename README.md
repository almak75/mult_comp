# Таблица умножения для младших школьников. 
Предназначена для облегчения изучения таблицы умножения младшими школьниками. Поозволяет лучше запоминать, ускорять процесс и тренироваться на ошибка. Имеет 2 режима: режим **"обучение"** и режим **"соревнование"**

## Режим "Обучение" позволяет в настройках:
  1. указать на какое число умножаем: х1, х2, х3, х4, х5, х6, х7, х8, х9, х10.
  2. выбрать - изучаем деление/умножение/сразу обе операции/
  3. сколько примеров необходимо для тренировочной сессии [1,100]
  4. формат ввода ответа: можно вводить числом на клавиатуре (детям не очень), а можно выбрать их 4х предложенных.
  5. можно сделать так, чтобы в конце обучающей сессии, ребенку были предложены примеры в которых были ошибки.
  6. надо ли показывать правильный ответ, если дан ошибочный? этот параметр тоже можно указать. 

По окончании тренировочной сессии - будет выведена статистика: количетсво  правильных, ошибочных ответов, примеры с ошибками. Вся статистика запоминается в разделе "Результаты обучения". Там же при необходимости можно запустить тест по примерам, где были даны ошибочные ответы.
  
  **Важно:** статистика накапливается, пока открыта страница в браузере. Закрыли страницу статистика обнулилась.

## Режим "Соревнование". 
Соревнование должно проводиться среди группы учеников. Создайте список учеников, участвующих в соревновании и запишите его в файл 2b.txt. В этом случае при запуске сервиса или в настройках, можно будет выбрать того, кто участвует.
Авторизация без пароля и SMS (детям проще). Авторизация необходима, чтобы результаты учеников запоминались между сессиями и формировалась таблица с результатами соревнований.
В режиме "Соревнование" автоматически генерируются 30 примеров на всю таблицу умножения, исключая умножение на х1 и х10. Задача ученика - как можно быстрее дать ответ на примеры. Если ученик установил личный рекорд по времени, то его результат будет записан в таблицу с резулььтатами.

## Как установить и запустить
1. git clone https://github.com/almak75/mult_comp.git
2. pip install -r requirements.txt
3. streamlit run start.py

## Попробовать
http://45.141.103.180:8501/

Для теста можно использовать учетную запись "Гость".


# Multiplication table for younger students.
Designed to facilitate the study of the multiplication table by younger students. It allows you to better remember, speed up the process and train for a mistake. Has 2 modes: **"Training"** mode and **"Competition"** mode

## The "Training" mode allows in the settings:
   1. indicate what number we multiply: x1, x2, x3, x4, x5, x6, x7, x8, x9, x10.
   2. choose - we study division / multiplication / both operations at once /
   3. how many examples are needed for a practice session [1,100]
   4. answer input format: you can enter a number on the keyboard (not for children), or you can choose 4 of them offered.
   5. You can make sure that at the end of the training session, the child is offered examples in which there were errors.
   6. Is it necessary to show the correct answer if an erroneous one is given? this option can also be specified.

At the end of the training session, statistics will be displayed: the number of correct, erroneous answers, examples with errors. All statistics are stored in the "Learning Results" section. In the same place, if necessary, you can run a test using examples where erroneous answers were given.
  
   **Important:** statistics are accumulated while the page is open in the browser. Closed the page statistics reset.

## "Competition" mode.
The competition must be held among a group of students. Create a list of students participating in the competition and write it to the 2b.txt file. In this case, when starting the service or in the settings, it will be possible to select who participates.
Authorization without a password and SMS (it's easier for children). Authorization is necessary so that the results of students are remembered between sessions and a table with the results of the competition is formed.
In the "Competition" mode, 30 examples are automatically generated for the entire multiplication table, excluding multiplication by x1 and x10. The task of the student is to answer the examples as quickly as possible. If the student has set a personal record in time, then his result will be recorded in the table with the results.

## How to install and run
1. git clone https://github.com/almak75/mult_comp.git
2. pip install -r requirements.txt
3. streamlit run start.py

## Test
http://45.141.103.180:8501/
