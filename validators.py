import re

def validate_email(email):
    # Email regular expressions, make sure to include @, . and university.com
    pattern = r"[^@]+\.+[^@\.]+@[^@\.]+\.[^@]+"
    return bool(re.match(pattern, email)) and 'university.com' in email

def validate_password(password):
    # Password regular expression, make sure it starts with a capital letter, at least 6 letters, followed by at least 3 numbers
    pattern = r"^[A-Z][a-zA-Z]{5,}\d{3,}$"
    return bool(re.match(pattern, password))
