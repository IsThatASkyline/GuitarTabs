from .user import CreateUserDTO, UserDTO, UpdateUserDTO
from .band import (
    CreateBandDTO,
    BandDTO,
    UpdateBandDTO,
    FullBandDTO,
)
from .song import (
    CreateSongDTO,
    SongDTO,
    UpdateSongDTO,
    FullSongDTO,
    ModulateSongDTO,
    FavoriteSongDTO,
    FindSongDTO,
    GetSongDTO,
)
from .verse import BaseVerseDTO
from .hit_counter import HitDTO, BaseHitDTO, CreateHitDTO
from .tab import BaseTabDTO, TabDTO, CreateTabDTO
