from setuptools import setup


VERSION = (0, 0, 1, "")

requirements = [
    "SQLAlchemy==0.9.7"
]

# TODO: Figure out how to ship regular files (not templated) with this setup
# TODO: That way, sdist doesn't try to byte-compile the python file templates.
setup(
    name="anodyne",
    description="Autonomous World Engine",
    packages=["anodyne"],
    version=".".join(filter(None, map(str, VERSION))),
    author="Alex Milstead",
    author_email="alex@amilstead.com",
    install_requires=requirements,
    package_dir={"anodyne": "anodyne"},
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
    ],
)
