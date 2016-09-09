import bcrypt

class PasswordService():
	def encrypt_password(password):
		return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

	def decrypt_password(password, password_hash):
		return bcrypt.checkpw(password.encode('utf-8'), password_hash)