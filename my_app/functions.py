from django.contrib.auth.models import User, Group

def lenstring(password):
    return len(password) < 8

def email_check(email):
    return User.objects.filter(email=email).exists()

def username_check(username):
    return User.objects.filter(username=username).exists()

def confirmation_password(password_1, password_2):
    return password_1 != password_2