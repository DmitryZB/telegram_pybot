# telegram_pybot

# Описание алгоритма сбора данных
Программа состоит из двух функций: первая функция “Parser_bot”
принимает на вход номер страницы на сайте, на которой имеется информация 
о 10 предметах, ID чата и значения фильтров поиска, вторая функция “Scanner”
получает на вход url со всей необходимой информацией отдельно взятого 
предмета, его наименование, url на сайте, user-agent, сгенерированный с 
помощью модуля fake-useragent, ID чата для отправления сообщения в случае, 
если предмет соответствует критериям, номер страницы, а также фильтры 
поиска.
Функция “Parser_bot” с помощью модуля requests получает HTML код, в 
котором скрипт выделяет ссылки на все предметы заданной страницы, затем в 
цикле с помощью модуля selenium, программа эмулирует переход 
пользователя по ссылке предмета, затем после подгрузки сайтом информации 
о предмете, программа выделяет уникальный ID предмета, через который 
генерируется ссылка со всей необходимой информацией, затем эта ссылка 
передается в качестве параметра в функцию “Scanner”
Функция “Scanner” с помощью модуля requests получает HTML код 
страницы предмета, откуда программа выделяет нужные данные: первый лот 
на продажу, первый лот на покупку, количество лотов на продажу, количество 
лотов на покупку, затем делает проверку с учетом пользовательских фильтров 
в случае, когда предмет является искомым – выводит сообщение с 
информацией о нем в соответствующий чат.

# Описание алгоритма телеграм бота
Программа телеграм бота обернута в одну функцию “telegram_bot” в 
которой определены условные функции, срабатывающие при получении 
определенной команды. С самого начала запуска бота, он уведомляет всех 
пользователей с правами доступа о своем включении и о готовности работать.
Функция “start” выводит приветствие, если пользователь, отправивший 
сообщение имеет права доступа, в противном случае уведомляет пользователя 
об отсутствии прав на использование бота.
Функция “stop” завершает работу бота и выводит соответствующее 
завершению работы сообщение.
Функция “settings” выводит краткую инструкцию по настраиваемым 
фильтрам, затем передает полученное сообщение функции “handler”
Функция “handler” проверяет введенную пользователем команду и 
вызывает соответствующую введенному параметру функцию, если команда, 
введенная пользователем, не входит в перечень команд – программа 
возвращается в начало с сообщением о неверно введенной команде.
Функции “change_interval”, “change_benefit”, “change_profit” 
вызываются функцией “handler” и позволяют соответственно изменять 
значение фильтров страничного диапазона, минимальной процентной 
разницы и минимальной прямой разницы.
Функция “send_text” вызывается в последнюю очередь, в зависимости от 
текста сообщения, вызвавшего эту функцию, она запускает программу 
парсера, выводит информацию о работе с ботом, останавливает процесс 
парсинга или выводит сообщение о неверной команде.
