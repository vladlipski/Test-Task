from django.contrib.auth.hashers import make_password


def encrypt_password(func):

    def wrapper(*args, **kwargs):
        request = args[1]
        data = request.data
        if 'password' in data:
            data['password'] = make_password(data['password'])
        return func(*args, **kwargs)

    return wrapper