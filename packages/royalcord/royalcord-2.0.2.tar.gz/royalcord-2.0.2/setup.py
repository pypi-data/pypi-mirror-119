from setuptools import setup
import re

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = ""
with open("discord/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("version is not set")


with open("README.md") as f:
    readme = f.read()

extras_require = {
    "voice": ["PyNaCl>=1.3.0,<1.5"],
    "docs": [
        "sphinx==4.0.2",
        "sphinxcontrib_trio==1.1.2",
        "sphinxcontrib-websupport",
    ],
    "speed": [
        "orjson>=3.5.4",
    ],
}

packages = [
    "discord",
    "discord.types",
    "discord.ui",
    "discord.webhook",
    "discord.ext.commands",
    "discord.ext.tasks",
]

setup(
    name="royalcord",
    author="Mythical-Studio & Rapptz",
    url="https://github.com/Mythical-Studio/RoyalCord",
    project_urls={
        "Issue tracker": "https://github.com/Mythical-Studio/RoyalCord/issues",
    },
    version=version,
    packages=packages,
    license="MIT",
    description="An API wrapper for Discord written in Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires=">=3.8.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
