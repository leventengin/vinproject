from .models import User


def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_pin(length=6):
    s = id_generator()
    while MyModel.objects.filter(pin=s).exists():
        print("pin generated",s)
        s = id_generator()
    return s



