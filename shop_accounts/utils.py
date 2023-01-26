from django.core.mail import send_mail

def send_activation_code(email, activation_code):
    message = f'Ваш код для активации аккаунта: {activation_code}'
    send_mail(
        'Activation',
        message,
        'babybaby_baby_oooo@gmail.com',
        [email]
    )