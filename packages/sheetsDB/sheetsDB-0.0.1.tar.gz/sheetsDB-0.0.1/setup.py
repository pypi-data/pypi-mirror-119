from setuptools import setup

setup(name='sheetsDB',
      version='0.0.1',
      packages=['sheetsDB'],
      author_email='fedor.tryfanau@gmail.com',
      zip_safe=False,
	  requires = [
    "gspread",
    "oauth2client"
]



)