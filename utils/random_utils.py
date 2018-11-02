import random
import string

def get_email_captcha():
    base = list(string.digits)
    captcha = "".join(random.sample(base, 6))
    return captcha

def get_random_name():
    base = list(string.ascii_lowercase)
    random_name = "".join(random.sample(base, 10))
    return random_name

if __name__ == "__main__":
    print(get_random_name())