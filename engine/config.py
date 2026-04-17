from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    width: int = 800
    height: int = 600


config = Config()
