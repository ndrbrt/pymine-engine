from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pymine-engine',
    version='0.1.0',
    url='https://github.com/ndrbrt/pymine-engine',
    license='MIT',
    author='Andrea Bertoloni',
    author_email='contact@andreabertoloni.com',
    description='API for implementing Minesweeper logic in Python',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Games/Entertainment :: Puzzle Games',
    ],
    packages=['pymine']
)
