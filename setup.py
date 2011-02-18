from setuptools import setup

readme = open('README.rst', 'r')
README_TEXT = readme.read()
readme.close()

setup(
    name='pivottable',
    packages=['pivottable'],
    version='0.8',
    description='A module that will help you to generate Pivot Tables base on arbitrary objects',
    long_description=README_TEXT,
    author='Mariano Mara',
    author_email='mariano.mara@gmail.com',
    url='https://bitbucket.org/marplatense/python-pivottable',
    download_url='https://bitbucket.org/marplatense/python-pivottable/downloads',
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords = ['pivot', 'table', 'pivottable', 'python']
    ,install_requires=['ordereddict']
)
