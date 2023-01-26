from django.core.mail import send_mail

def send_activation_code(email, activation_code):
    message = f'Congrats u won the lottery click here to get your price. Send us this code {activation_code}'
    send_mail(
        'Activation',
        message,
        'babybaby_baby_oooo@gmail.com',
        [email]
    )