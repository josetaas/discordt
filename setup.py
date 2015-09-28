from codecs import open as codecs_open
from setuptools import setup, find_packages

setup(name='discordt',
      version='0.0.1',
      description=u"Discord Terminal Client",
      classifiers=[],
      keywords='',
      author=u"Jose Francisco Taas",
      author_email='josetaas@gmail.com',
      url='https://github.com/mapbox/discordt',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'python-dateutil',
          'discord.py',
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      discordt=discordt.scripts.discordt:main
      """
      )
