@app.route("/payout", methods=['GET', 'POST'])
@login_required
def payout():

    # 1 Создаем платеж
    # 2 Добавляем его в базу данных, сразу же с полями id, login, orderid, amount, description
    # 3 После проведения платежа смотри его статус в зависимости от переадресации
    # 4 Если статус заказа True, то меняем его в базе данных и пользователю активируем подписку
    # 5 Если статус заказа False, то пишем что платеж не пришел и не активируем подписку

    # Получаем Данные от банка
    TEST_TERMINAL_KEY = ''
    TEST_SECRET_KEY = ''
    orderid = str(uuid4())
    init_post_data = {'TerminalKey': TEST_TERMINAL_KEY,
                      'Amount': 1000,
                      "Customer": current_user.id,
                      'OrderId': orderid,
                      'Description': "Платеж"}
    init_url = "https://securepay.tinkoff.ru/v2/Init"
    new_order = Payment(login=current_user.login, success=False, orderid=orderid, description="Платеж)
    db.session.add(new_order)
    db.session.commit()
    init_rq = requests.post(init_url, json=init_post_data)
    init_rq_json = init_rq.json()
    print(init_rq_json)
    return "Yes"

@app.route("/success", methods=['GET', 'POST'])
@login_required
def success():
    # Успешный ответ
    print(request.args)
    orderid = request.args.get("OrderId")
    status = request.args.get("Success")
    if status == "true":
        if Payment.query.filter_by(orderid=orderid).first():
            payment = Payment.query.filter_by(orderid=orderid).first()
            payment.success = True
            db.session.commit()

            login = payment.login
            user = User.query.filter_by(login=login).first()
            print(datetime.now())
            print(user.login)
            user.dataOrder = datetime.now()
            db.session.commit()

            return "Все успешно"

    status = request.args.get("ErrorCode")
    return status

@app.route("/error", methods=['GET', 'POST'])
@login_required
def error_payout():
    # Ответ с ошибокй
    print(request.args)
    error_message = request.args.get("Message")
    return error_message
