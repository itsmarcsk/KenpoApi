import bcrypt

class PasswordEncryptor:
    @staticmethod
    def hash_password(password: str) -> str:
        # Generar un salt
        salt = bcrypt.gensalt()
        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        # Devolver la contraseña hasheada como una cadena
        return hashed_password.decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        # Comprobar si la contraseña coincide con el hash
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))