from paver.easy import *
from paver.path import path
from paver.setuputils import setup


VERSION = (0, 0, 1, "")

with open("dependencies.pip") as dependencies:
    install_requires = [
        dep.replace(",", "")
        for dep in dependencies.read().splitlines()
    ]


# TODO: Figure out how to ship regular files (not templated) with this setup
# TODO: That way, sdist doesn't try to byte-compile the python file templates.
setup(
    name="awengine",
    description="Autonomous World Engine",
    packages=["anodyne"],
    version=".".join(filter(None, map(str, VERSION))),
    author="Alex Milstead",
    author_email="alex@amilstead.com",
    install_requires=install_requires,
    package_dir={
        "anodyne": "anodyne"
    },
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
    ],
)

MANIFEST = (
    "include setup.py",
    "include paver-minilib.zip",
)

@task
def manifest():
    path("MANIFEST.in").write_lines("%s" % x for x in MANIFEST)


@task
@needs(
    "generate_setup",
    "minilib",
    "manifest",
    "setuptools.command.sdist"
)
def sdist():
    pass


@task
def clean():
    for p in map(path, (
        "anodyne.egg-info", "dist", "build", "MANIFEST.in", "docs/build")):
        if p.exists():
            if p.isdir():
                p.rmtree()
            else:
                p.remove()
    for p in path(__file__).abspath().parent.walkfiles():
        if p.endswith(".pyc") or p.endswith(".pyo"):
            p.remove()


@task
def docs():
    # have to touch the automodules to build them every time since changes to
    # the module"s docstrings won"t affect the timestamp of the .rst file
#    sh("find docs/source/awengine -name *.rst | xargs touch {}")
    sh("find docs/source -name *.rst -exec touch \"{}\" \\;")
    sh("cd docs; make html")


@task
def test():
    # TODO: Turn test dir into real unit tests.
    #sh("nosetests test/unit test/functional")
    pass