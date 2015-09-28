from setuptools import setup, find_packages
import re

version = ''
with open('discordt/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(name='discordt',
      version=version,
      description=u"Discord Terminal Client",
      classifiers=[],
      keywords='',
      author=u"Jose Francisco Taas",
      author_email='josetaas@gmail.com',
      url='https://github.com/jftaas/discordt',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'python-dateutil',
          'discord.py',
      ],
      entry_points="""
      [console_scripts]
      discordt=discordt.cli:main
      """
      )
