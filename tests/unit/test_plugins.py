import  SubtitleToAudio.plugins
from  SubtitleToAudio.core import discover_plugins


def test_plugins():
    plugins = discover_plugins( SubtitleToAudio.plugins)

    assert len(plugins) == 1
