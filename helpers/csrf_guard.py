from functools import wraps
from secrets import token_urlsafe
from flask import session, request

CSRF_TOKEN_KEY = "CSRF_TOKEN"


def csrf_token():
	"""
	Function for use in forms, generates a new CSRF token or retrieves
	the current token if one exists.
	:return: The CSRF secret token
	"""
	if CSRF_TOKEN_KEY in session:
		return session[CSRF_TOKEN_KEY]
	csrf_val = get_new_csrf()
	session[CSRF_TOKEN_KEY] = csrf_val
	return csrf_val


def get_new_csrf():
	"""
	Generates and returns a 50 byte CSRF secret
	:return: The CSRF secret token
	"""
	return str(token_urlsafe(50))


def validate_csrf(func):
	"""
	Decorator that handles CSRF validation for forms
	:param func: The function being wrapped
	:return: Function wrapped with CSRF checks
	"""
	@wraps(func)
	def inner(*args, **kwargs):
		if CSRF_TOKEN_KEY not in session:
			session[CSRF_TOKEN_KEY] = get_new_csrf()
			return "No CSRF token set, please try again."
		form_csrf_val = request.form.get(CSRF_TOKEN_KEY)
		if not form_csrf_val == session[CSRF_TOKEN_KEY]:
			session[CSRF_TOKEN_KEY] = get_new_csrf()
			return "Invalid CSRF token, please try again."
		session[CSRF_TOKEN_KEY] = get_new_csrf()
		return func(*args, **kwargs)
	return inner
