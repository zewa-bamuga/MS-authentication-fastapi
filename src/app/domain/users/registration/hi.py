import random
import smtplib
import string
from email.message import EmailMessage

from app.domain.common.models import User


def Generate_Password(min_length=8, max_length=8):
    length = random.randint(min_length, max_length)
    password = generate_valid_password(length)
    return password


def generate_valid_password(length):
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    if not any(char.isdigit() for char in password):
        return generate_valid_password(length)
    if not any(char.islower() for char in password):
        return generate_valid_password(length)
    if not any(char.isupper() for char in password):
        return generate_valid_password(length)

    return password


async def First_Registration(email: str, password: str):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Подтверждение регистрации"
    msg['From'] = email_address
    msg['To'] = email

    html_content = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
            <h2 style="color: #FFD700;">Подтверждение регистрации</h2>
            <p>Дорогой сотрудник Отдела Образовательных Программ!</p>
            <p>Мы рады приветствовать тебя на платформе ООП. Твой пароль для входа:</p>
            <p style="font-size: 18px; font-weight: bold; color: #FFD700;">{password}</p>
            <p>Твой Отдел Образовательных Программ <span style="color: #FFD700;">&lt;3</span></p>
            <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
        </div>
    </body>
    </html>
    """

    msg.set_content(
        "Дорогой сотрудник Отдела Образовательных Программ! Мы рады приветствовать тебя на платформе ООП. Твой пароль для входа: {password}. Твой Отдел Образовательных Программ <3")
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


async def send_hello(user: User):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Подтверждение регистрации"
    msg['From'] = email_address
    msg['To'] = user.email

    html_content = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
            <h2 style="color: #FFD700;">Подтверждение регистрации</h2>
            <p>Дорогой пользователь платформы Отдела Образовательных Программ!</p>
            <p>Мы рады приветствовать тебя!</p>
            <p>Твой Отдел Образовательных Программ <span style="color: #FFD700;">&lt;3</span></p>
            <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
        </div>
    </body>
    </html>
    """

    msg.set_content(
        "Дорогой пользователь платформы Отдела Образовательных Программ! Мы рады приветствовать тебя! Твой Отдел Образовательных Программ <3")
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


async def send_user_email_verification(email: str, code: int):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Подтверждение почты"
    msg['From'] = email_address
    msg['To'] = email

    html_content = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
            <h2 style="color: #FFD700;">Сброс пароля</h2>
            <p>Здравствуйте,</p>
            <p>Подтверждение почты на платформе Отдела Образовательных Программ.</p>
            <p>Код для подтверждения почты:</p>
            <p style="font-size: 18px; font-weight: bold; color: #FFD700;">{code}</p>
            <p>Если вы не запрашивали подтверждения почты, проигнорируйте это письмо.</p>
            <p>С уважением,<br>Ваш Отдел Образовательных Программ</p>
            <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
        </div>
    </body>
    </html>
    """

    msg.set_content(
        f"Здравствуйте,\n\nВы запросили сброс пароля на платформе Отдела Образовательных Программ.\n\nКод для сброса пароля: {code}\n\nЕсли вы не запрашивали сброс пароля, проигнорируйте это письмо.\n\nС уважением,\nВаш Отдел Образовательных Программ"
    )
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


async def send_password_reset_email(email: str, code: str):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"

    msg = EmailMessage()
    msg['Subject'] = "Сброс пароля"
    msg['From'] = email_address
    msg['To'] = email

    html_content = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #003366; background-color: #486DB5;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background-color: #ffffff;">
            <h2 style="color: #FFD700;">Сброс пароля</h2>
            <p>Здравствуйте,</p>
            <p>Вы запросили сброс пароля на платформе Отдела Образовательных Программ.</p>
            <p>Код для сброса пароля:</p>
            <p style="font-size: 18px; font-weight: bold; color: #FFD700;">{code}</p>
            <p>Если вы не запрашивали сброс пароля, проигнорируйте это письмо.</p>
            <p>С уважением,<br>Ваш Отдел Образовательных Программ</p>
            <p style="margin-top: 20px; color: #777; font-size: 12px;">Если у вас возникли какие-либо вопросы, пожалуйста, свяжитесь с нами.</p>
        </div>
    </body>
    </html>
    """

    msg.set_content(
        f"Здравствуйте,\n\nВы запросили сброс пароля на платформе Отдела Образовательных Программ.\n\nКод для сброса пароля: {code}\n\nЕсли вы не запрашивали сброс пароля, проигнорируйте это письмо.\n\nС уважением,\nВаш Отдел Образовательных Программ"
    )
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


async def lol(email: str, code: str):
    email_address = "tikhonov.igor2028@yandex.ru"
    email_password = "abqiulywjvibrefg"
    # code = PasswordResetCode.generate_code()

    msg = EmailMessage()
    msg['Subject'] = "Сброс пароля"
    msg['From'] = email_address
    msg['To'] = email
    msg.set_content(
        f"""\
        Здравствуйте,

        Вы запросили сброс пароля на платформе Путеводитель по необычным местам.

        Код для сброса пароля: {code}

        Если вы не запрашивали сброс пароля, проигнорируйте это письмо.

        С уважением,
        Ваша команда Путеводитель по необычным местам
        """
    )

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
