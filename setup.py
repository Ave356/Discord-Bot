from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Discord-Bot',
    author="Ave356",
    author_email=".",
    url="https://github.com/Ave356/Discord-Bot",
    version='0.0.1',
    packages=['Discord-Bot'],
    license='MIT License',
    long_description=readme(),
    long_description_content_type='test/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'discord',
        'discord.py',
        'discordbot.py',
        'youtube-dl',
        'PyNaCl',
        'discord.py[voice]',
    ],
)
