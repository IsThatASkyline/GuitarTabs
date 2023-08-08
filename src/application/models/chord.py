from dataclasses import dataclass


@dataclass(frozen=True)
class Chord:
    name: str
