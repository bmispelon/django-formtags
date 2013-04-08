from setuptools import setup, find_packages

setup(
    name="django-formtags",
    version="0.1.1",
    description="Customize form fields directly from templates",
    keywords="django, forms, tags",
    author="Baptiste Mispelon",
    author_email="bmispelon@gmail.com",
    url="https://github.com/bmispelon/django-formtags/",
    license="BSD",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3"
    ],
)
