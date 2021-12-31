from setuptools import setup

setup(
    name='FockNews',
    version='0.4.1CSU',
    packages=['API', 'API.migrations', 'Main', 'Main.migrations', 'Users', 'Users.migrations', 'FockNews',
              'html_forms'],
    url='http://vk.com/onlikerop/',
    license='Private',
    author='Eugene Karabanov',
    author_email='onlikerop@email.cz',
    description='News website based on Django'
)
