

class FileNotSupported(Exception):
    def __init__(self, fname: str) -> None:
        self.fname = fname
        super().__init__(f'File [{self.fname}] not supported!!')