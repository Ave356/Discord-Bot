from setuptools import setup

setup(
    name='Discord-Bot',
    author="Ave356",
    author_email=".",
    url="https://github.com/Ave356/Discord-Bot",
    version='0.1dev',
    packages=['Discord-Bot',],
    license='MIT License',
    long_description=open('README').read(),
    platforms="Platform agnostic",
    install_requires=[
        'discord==1.0.1',
        'discord.py==1.3.3',
        'discordbot.py==0.2.3a3',
        'youtube-dl==2020.5.8'
        'PyNaCl==1.3.0',
        'discord.py[voice]',
    ],
)
