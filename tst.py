from Validate import Validate

username = "Dogman1!"
password = "dog1%44D"

validate = Validate(username)
print(validate.validate_username())
validate = Validate(password)
print(validate.validate_password())
