from setuptools import setup, find_packages
from POS.constants import APP_NAME

setup(
    name=APP_NAME,
    version="1.0.0",
    description="An online pay-as-you-go Point Of Sale System",
    long_description=open("README.md").read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==6.7",
        "decorator==4.2.1",
        "Flask==0.12.2",
        "ipython==6.2.1",
        "ipython-genutils==0.2.0",
        "itsdangerous==0.24",
        "jedi==0.11.1",
        "Jinja2==2.10",
        "MarkupSafe==1.0",
        "parso==0.1.1",
        "pexpect==4.4.0",
        "pickleshare==0.7.4",
        "prompt-toolkit==1.0.15",
        "psycopg2-binary==2.7.4",
        "ptyprocess==0.5.2",
        "pyaml==17.12.1",
        "Pygments==2.7.4",
        "PyYAML==3.12",
        "simplegeneric==0.8.1",
        "six==1.11.0",
        "SQLAlchemy==1.2.5",
        "traitlets==4.3.2",
        "wcwidth==0.1.7",
        "Werkzeug==0.14.1"
    ],
    author="Eddy Mwenda, Jeff Ndungu, Catherine Nyambura",
    author_email="mwendaeddy@gmail.com, jeffkim207@gmail.com, cnyambura043@gmail.com",
)
