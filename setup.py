import os
import re
import sys
from io import open

from setuptools import find_packages, setup


def read(f):
    return open(f, 'r', encoding='utf-8').read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


version = get_version('djf_surveys')


def build_package():
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    # Compile translations and collect static assets.
    os.system("cd djf_surveys && python ../demo/manage.py compilemessages && python ../demo/manage.py collectstatic --noinput -c --settings demo.settings")
    os.system("python setup.py sdist bdist_wheel")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        print("Try using `pip install -U twine wheel`.\nExiting.")
        sys.exit()


if sys.argv[-1] == 'publish':
    build_package()
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


if sys.argv[-1] == 'build_pre_publish':
    build_package()
    print("The version now: ", version)
    sys.exit()


setup(
    name='django-form-surveys',
    version=version,
    url='https://irfanpule.github.io/django-form-surveys',
    license='MIT License',
    description='A simple Django app to conduct Web-based survey',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='irfanpule',
    author_email='irfan.pule2@gmail.com',
    packages=get_packages('djf_surveys'),
    include_package_data=True,
    install_requires=["django>=2.2", "pytz"],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
