__author__ = 'axclgo'

from dotenv import load_dotenv
import os
load_dotenv()


print(os.getenv('AWS_ACCESS_KEY_ID'))
