from setuptools import setup

setup(
  name='sqla-softdelete',
  packages=['sqla-softdelete'],
  version='0.1',
  license='GPLv3+',
  description='SQLAlchemy soft delete',
  author='Vitaly Efremov',
  author_email='efremov.vitaly@gmail.com',
  url='https://github.com/vitaly-efremov/sqla-softdelete',
  download_url='https://github.com/vitaly-efremov/sqla-softdelete/archive/0.1.tar.gz',
  keywords=['SQLAlchemy', 'Soft delete'],
  install_requires=[ 
          'sqlalchemy',
          'pytest',
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)