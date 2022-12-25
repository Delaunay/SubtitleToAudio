"""Top level module for  SubtitleToAudio"""

import importlib
import json
import pkgutil

import importlib_resources

__descr__ = "Simple script to turn Subtitles to audio"
__version__ = "0.0.1"
__license__ = "BSD 3-Clause License"
__author__ = "Pierre Delaunay"
__author_email__ = "admin@gamekit.ca"
__copyright__ = "2022 Pierre Delaunay"
__url__ = "https://github.com/Delaunay/SubtitleToAudio"


def discover_plugins(module):
    """Discover uetools plugins"""
    path = module.__path__
    name = module.__name__

    plugins = {}

    for _, name, _ in pkgutil.iter_modules(path, name + "."):
        plugins[name] = importlib.import_module(name)
        print(f" - Found plugin: {name}")

    return plugins


data_path = importlib_resources.files(" SubtitleToAudio.data")

with open(data_path / "data.json", encoding="utf-8") as file:
    print(json.dumps(json.load(file), indent=2))
