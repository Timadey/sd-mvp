from dataclasses import dataclass

@dataclass
class CreateUserDTO:
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    email: str
    role: str

class LoginDTO:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password