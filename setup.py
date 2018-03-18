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
        "Flask==0.12.2",
        "itsdangerous==0.24",
        "Jinja2==2.10",
        "MarkupSafe==1.0",
        "Werkzeug==0.14.1",
        "psycopg2-binary==2.7.4",
        "SQLAlchemy==1.2.5",
    ],
    author="Eddy Mwenda, Jeff Ndungu, Catherine Nyambura",
    author_email="mwendaeddy@gmail.com, jeffkim207@gmail.com, cnyambura043@gmail.com",
)
