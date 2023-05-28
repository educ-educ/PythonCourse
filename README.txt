problems - папка с задачами (условия, тесты, ответы)
reader, userdata - используются/использовавались server.py

server.py - сервис проверки решения задач
# GET # /api/allproblems - возвращает все задачи (название + условие)
# GET # /api/problems/<problem_id> - получение той же информации по одной задаче
# GET # /api/tests/<problem_id>/<test_id> - получение теста test_id задачи problem_id
# GET # /api/answers/<problem_id>/<test_id> - получение ответа к тесту test_id задачи problem_id
# POST # /api/check/<problem_id>/<user_id> - проверить решение задачи участника

checker.py - не используется

registration-service - сервис регистрации курсов, получение информации о них
# GET # /send-test-json-to-create/ - создать новый тестовый курс (никакие поля заполнять не надо, они прописаны)
# GET # /send-test-json-to-update/<ind> - обновить курс id = <ind> тестовой информацией
# POST # /course/create - создать новый курс (возвращается id)
# POST # /course/update/<ind> - обновить курс с id = <ind>
# GET # /course/get-all - получить все курсы
# GET # /course/get-by-id/<id> - получить курс с id = <ind>
# GET # /course/remove/<id> - удалить курс с id = <ind>