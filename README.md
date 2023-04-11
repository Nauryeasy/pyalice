Итак, моя первая (недо) библиотека для создания навыков Алисы
Для начала хочу попросить не осуждать меня за код, странные решенияи тому подобное, эта библиотека была создана мной ради удовольствия,
но все же помогла создавать мне навыки. Некоторые технические решения были придуманы elogrus, за что ему большое спасибо.

Пока что будет описана лишь небольшая часть библиотеки из небольшой написаной, более подробное описание всего, что я накарябал будет выложена с примерами
использования позже. Так же она будет по возможности улучшаться и становиться более дружелюбной.


Dialog - класс диалога.

Поля:
1) next_states_list: список диалогов, в которые можно будет из него перейти.
2) get_response - функию, которая будет возвращать текст сообщения поля для response такие как: text, tts, buttons, card(По желанию),
session_state(По желанию), user_state_update(По желанию)
3) tokens - слова-триггеры для данного диалога (Максимально корявая штука, нужно придумать что-то другое)
4)last_state - предыдущий диалог, изначально None. (Нужно для кнопок по типу "назад", но в связи с возникшими багами иногда работает некорректно для middleware_dialog,
в связи с чем не рекомендую к использованию)
5) always - неудавшийся эксперемент, который нужен был для того, чтобы диалог триггерился в любом случае, несмотря на tokens
Сейчас это реализуется через состояния, после того как выйдет более подробное описание и примеры, это будет понятнее.
Иногда можно использовать для некоторых диалогов, но только тех, которые должны триггериться ВООБЩЕ всегда.

Методы:
1) get_response_info - метод, который вызывает метод get_response переданный в параметрах и возвращает его результат
2) set_last_state - метод устанавливающий предыдущий диалог
3) set_next_states_list - метод устанавливающий список следующих диалогов
4) set_always - метод меняющий поле always (Абсолютно не нужен и будет вырезан)

У этого класса есть наследник - TimeoutDialog, который служит для того, чтобы отправить пользователю ответ, на получение которого уходит больше времени,
чем доступное для Алисы.
Наследник StartDialog отличается лишь тем, что его последнее состояние это он сам.


Handler - основной класс навыка. В нем будут выбираться диалоги которые нужны в данный момент и он будет отдавать ответ.

Поля:
1) dialogs_dict - словарь с парами "состояние" - "диалог", где ключом будет являться состояние, которое будет устанавливать диалог, а значением сам объект
класса Dialog
2) middleware_dialog_list - список с диалогами, которые должны вызываться из любой точки навыка
3) start_dialog - объект класса Dialog, который является входной точкой в навык

Методы:
1) choose_dialog - метод, который будет выбирать нужный диалог и возвращать его ответ, в случае если ни один диалог не выбран возвращается сообщение по типу:
"Не поняла"
2) staticmethod get_state - возвращает текущее состояние
3) staticmethod check_tokens - возвращает True, если tokens находяться в запросе
4) staticmethod check_new_session - метод, который возвращает True, в случае если это первый запрос в навык в текущей сессии


Response - класс, который формирует ответ. С данным классом взаимодействует Handler, трогать его нужно только чтобы что-то в нем изменить, если нужен доп. функционал или если написаный мной является корявой фигней.

Поля:
1) event - запрос пользователя
2) dialog - Объект класса диалог, который будет давать ответ пользователю

Методы:
1) get_response - по типу диалога определяет, какую фунцию для формирования ответа нужно вызвать и возвращает ее резульатат.
2) get_response-dialog - функция которая вызывается о обычного диалога, вызывает у self.dialog функцию get_response_info и формирует ответ пользователю
3) get_response_start_dialog - была создана для того, чтобы сделать авторизацию в навыке "Менеджер музыки", для которого была написана (недо) библиотека,
но в связи с тем, что авторизацию пришлось менять с встроеной в Яндекс Диалоги на свою, этот диалог ничем не отличается от обыкновенного. Если нужна будет
авторизация можно добавить пару строк и будет готово. Ну или какие-либо другие фишки для стартового диалога.
4) get_response_timeout_dialog - аналогично get_response_start_dialog
5) staticmethod create_buttons - метод формирует кнопки из тех, которые вернул self.dialog.get_response_info
6) is_authorize - метод проверяет, авторизирован ли пользователь. Данный метод проверяет, есть ли access_token в сессии запроса.



Для работы нужно создать объекты класса Dialog со всеми необходимыми параметрами, распределить, если это нужно, на обычные и middleware_dialog, создать объект класса Handler со всеми необходимыми параметрами и на запрос пользователя отвечать результатом функции choose_dialog у объекта класса Handler.


Возвращаясь к полю always, которое не стоит использовать, для диалогов, которые должны повториться несколько раз, например запросить информацию у пользователя, когда он сделает несколько ответов, стоит в 'session_state' передать любое значение по ключу названия состояния диалога. Пока это значение будет передаваться в состоянии диалог будет тригерриться бесконечно. Это можно будет увидеть в примераз, которые выйдут чуть позже.
Точка.
