from setuptools import setup, find_packages

setup(
    name='mlbattendanceplotter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'plotly',
    ],
    include_package_data=True,
    description='A plotting package for viewing MLB Stadium Attendance Trends (2012-2019)',
    author='Elliot Wolf',
)
