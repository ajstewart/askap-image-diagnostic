from setuptools import setup, find_packages

setup(name='racstransients',
      version='1.0.0',
      description='Search RACS fields for historical transients.',
      url='http://github.com/ajstewart/askap-image-diagnostic',
      author='Adam Stewart',
      author_email='adam.stewart@sydney.edu.au',
      license='',
      packages=find_packages(),
      install_requires=['numpy',
                        'astropy',
                        'matplotlib',
                        'AegeanTools',
                        'pandas',
                        'astroquery',
                        'colorlog',
                        'django<3.0,>=2.2.9',
                        'django_tables2',
                        'whichcraft',
                        # 'bdsf',
                        'sqlalchemy',
                        'psycopg2',
                        'tablib',
                        'django-contrib-comments',
                        'django-filter',
                        'django-crispy-forms',
                        'django-rest-auth',
                        'django-allauth',
                        'django-keyboard-shortcuts'
                        ],
      scripts=["bin/processASKAPimage.py"],
      dependency_links=[],
      include_package_data=True)
      