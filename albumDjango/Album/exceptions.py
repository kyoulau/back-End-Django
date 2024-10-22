class IDNotFoundException(Exception):
    def __init__(self, message="O ID fornecido não foi encontrado."):
        self.message = message
        super().__init__(self.message)