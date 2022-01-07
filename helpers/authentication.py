import uuid
from argon2 import PasswordHasher, profiles, exceptions
from helpers.db import Database
from flask_login import UserMixin

hasher = PasswordHasher.from_parameters(profiles.RFC_9106_HIGH_MEMORY)


class User(UserMixin):
	"""
	User class, stores information about a user's session
	"""
	def __init__(self, user_uuid):
		with Database() as db:
			self._user_data = db.get_user_by_uuid(user_uuid)
		self._active = True
		self._authenticated = True
		self._anonymous = False

	def is_authenticated(self):
		"""
		User is authenticated, always true if this object was created
		:return: True if user is authenticated, false otherwise
		"""
		return self._authenticated

	def is_active(self):
		"""
		User is active, always true if this object was created
		:return: True if the user is active, false otherwise
		"""
		return self._active

	def is_anonymous(self):
		"""
		User is anonymous, always returns false
		:return: false
		"""
		return self._anonymous

	def username(self):
		"""
		Returns the username for this session object
		:return: The user's username
		"""
		return self._user_data['username']

	def user_uuid(self):
		"""
		Returns the uuid of this user
		:return: The user's UUID
		"""
		return self._user_data['user_uuid']


def add_user(username, password):
	"""
	Adds a user to the database, generates the UUID and hashes the password
	:param username: The user's username to create
	:param password: The unhashed user password
	:return: Nothing
	"""
	user_uuid = str(uuid.uuid4())
	hashed_password = hasher.hash(password)
	with Database() as db:
		db.add_user(user_uuid, username, hashed_password)


def verify_user_login(username, password):
	"""
	Verify a username and password combination
	:param username: The username of the user to verify
	:param password: The unhashed password to verify
	:return: True if the combination is valid, False otherwise
	"""
	with Database() as db:
		user_data = db.get_user_by_username(username)
		if not user_data:
			return False
		try:
			return hasher.verify(user_data['hashed_password'], password)
		except exceptions.VerifyMismatchError:
			return False
		except Exception as e:
			print("Exception hashing: {}".format(e))
			return False
