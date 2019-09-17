from dotenv import load_dotenv
from os import environ

flask_env = environ.get('FLASK_ENV', None)
if not flask_env in ['heroku', 'deploying']:
    load_dotenv()
