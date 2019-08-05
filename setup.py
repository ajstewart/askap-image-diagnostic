from setuptools import setup, find_packages

setup(name='askap-image-diagnostic',
      version='0.8.1',
      description='Perform analysis tasks on ASKAP images.',
      url='http://github.com/ajstewart/askap-image-diagnostic',
      author='Adam Stewart',
      author_email='adam.stewart@sydney.edu.au',
      license='',
      packages=find_packages(),
      install_requires=['numpy',
                        'astropy',
                        'matplotlib',
                        'aplpy',
                        'AegeanTools',
                        'pandas',
                        'astroquery',
                        'colorlog',
                        'django < 2.0',
                        'django_tables2==2.0.5',
                        'whichcraft',
                        'bdsf',
                        'sqlalchemy',
                        'psycopg2',
                        'tablib',
                        'django-contrib-comments'
                        ],
      scripts=["bin/processASKAPimage.py"],
      dependency_links=['https://github.com/lofar-astron/PyBDSF/tarball/master#egg=bdsf-1.9.0'],
      include_package_data=True)
      