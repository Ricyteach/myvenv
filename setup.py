from setuptools import setup

setup(
    name='myvenv',
    version='0.1',
    py_modules=['myvenv'],
    install_requires=[
        'Click',
    ],
    extras_require = dict(
        dev = [
            'pytest',
        ]
    ),
    entry_points="""
        [console_scripts]
        myvenv=myvenv.cli:main
    """,
    url='https://github.com/Ricyteach/myvenv',
    license='MIT License',
    author='Ricky L Teachey Jr',
    author_email='ricky@teachey.org',
    description='Quickie setup of virtual environment customized to my preferences.  '
)
