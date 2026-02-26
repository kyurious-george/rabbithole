from abc import ABC, abstractmethod

# ─────────────────────────────────────────────────────────────────────────────
# Log Formatter
# ─────────────────────────────────────────────────────────────────────────────

class Formatter(ABC):
    @abstractmethod
    def format(self, message: str): 
        pass

class PlainFormatter(Formatter): 
    def format(self, message: str): 
        return message

class JSONFormatter(Formatter): 
    def format(self, message: str): 
        return {"log": message}

class Logger:
    def __init__(self, formatter: Formatter):
        self._formatter = formatter

    def log(self, message: str): 
        formatted_message = self._formatter.format(message)
        print(formatted_message)

# ─────────────────────────────────────────────────────────────────────────────
# Input Validator 
# ─────────────────────────────────────────────────────────────────────────────

class ValidatorService(ABC): 
    @abstractmethod
    def validate(self, input: str) -> bool:
        pass

    @property
    @abstractmethod
    def name(self) -> str: 
        pass

class PasswordValidator(ValidatorService): 
    NAME = "PASSWORD_VALIDATOR"

    def validate(self, input: str) -> bool: 
        if len(input) < 8: 
            return False
        return True 
    
    @property
    def name(self) -> str: 
        return self.NAME
    
class EmailValidator(ValidatorService): 
    NAME = "EMAIL_VALIDATOR"

    def validate(self, input: str) -> bool: 
        if '@' not in input: 
            return False
        return True
    
    @property
    def name(self) -> str: 
        return self.NAME

class RegistrationService:
    def __init__(self, validators: list[ValidatorService]): 
        self._validators = validators

    def register(self, input: str) -> list[bool]:
        results = []
        for validator in self._validators: 
            result = validator.validate(input)
            print(f"Validator: {validator.name}, Result: {result})")
            results.append(result)
        return results
    


if __name__ == "__main__":
#     plain_logger = Logger(PlainFormatter())
#     plain_logger.log("Server started on port 8080")

#     json_logger = Logger(JSONFormatter())
#     json_logger.log("Server started on port 8080")

    email_reg = RegistrationService([EmailValidator()])
    email_reg.register("user@example.com")  # Should pass
    email_reg.register("invalid-email")      # Should fail

    pass_reg = RegistrationService([PasswordValidator()])
    pass_reg.register("strongpassword")  # Should pass
    pass_reg.register("short")            # Should fail