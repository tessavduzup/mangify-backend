import smtplib
from email.mime.text import MIMEText


def send_cheque(recipient, order_number, order_sum, card_number, goods, time_date):
    goods_str = ""
    for good in goods:
        if good != goods[-1]:
            goods_str += f'"{good}", '
        else:
            goods_str += f'"{good}"'

    message = (f"Электронный чек заказа {order_number}\nБлагодарим вас за покупку! Сведения о покупке:\n\nНомер заказа:"
               f"{order_number}\nКупленные товары: {goods_str}\nСумма заказа: {order_sum} рублей\nДата и время покупки:"
               f"{time_date}\nКарта: *{card_number}\nКонтактная информация:\n\nКОНТАКТЫ")

    msg_object = MIMEText(message)
    msg_object['Subject'] = "Спасибо за покупку!"
    sender = "manfigy@mail.ru"
    password = "!ZV@ZV#ZV$ZV%ZV^"

    server = smtplib.SMTP("smtp.mail.ru", 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg_object.as_string())

        return "The message was sent"
    except Exception as ex:
        return f"{ex}"


def confirm_registration(recipient, username, code):
    message = MIMEText((f"Здравствуйте, {username}. Вы регистрируетесь в интернет-магазине Mangify. "
                        f"Для подтверждения электронной почты введите код,"
                        f"представленный ниже:\n\n{code}\n\nЕсли вы не регистрировались на сайте http://mangify.ru/, "
                        f"то проигнорируйте это письмо."))

    message['Subject'] = "Подтверждение почты"
    sender = "s.petrushin12@mail.ru"
    password = "yi21FCjmHW3nzgSL3Ezz"

    server = smtplib.SMTP("smtp.mail.ru", 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, recipient, message.as_string())

        return "The message was sent"
    except Exception as ex:
        return f"{ex}"


# print(confirm_registration("c1208@mail.ru", "tessavduzup", "123456"))
# print(send_cheque("c1208@mail.ru", "123123", 600, "3214",
#                   ["Магическая битва", "Говно ежа"], datetime.datetime.now().replace(microsecond=0)))