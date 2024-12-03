# functions.py
# Template from https://aierlab.tech/MultiverseNote/docs/en/getting_started.html

from __future__ import annotations

import typing as tp

def playAccompanimentTrackRealtimeTempo():
    print('Time for Yuxuan to bring it on!')

class MidiPlayer:
    singleton: MidiPlayer | None = None

    def __new__(cls) -> MidiPlayer:
        if cls.singleton is None:
            cls.singleton = super().__new__(cls)
        return cls.singleton
    
    def __init__(self):
        ...

FUNCTION_MAPPING = {
    "playAccompanimentTrackRealtimeTempo": playAccompanimentTrackRealtimeTempo,
    "search_duckduckgo": search_duckduckgo,  # Another mapped function.
}

TOOLS_DEFINE = [
    {
        "type": "function",
        "function": {
            "name": "fetch_web_page",
            "description": "Fetches and returns the content of a web page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the web page to fetch."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_duckduckgo",
            "description": "Simulates a simple DuckDuck Go search and returns the first result URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on DuckDuckGo."
                    }
                },
                "required": ["query"]
            }
        }
    }
]
