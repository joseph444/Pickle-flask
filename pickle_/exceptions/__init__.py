class FileNotFound(Exception):
    def __str__(self):
        return "There is Some Problem in loading the File"
    def __repr__(self):
        return "There is Some Problem in loading the File"
