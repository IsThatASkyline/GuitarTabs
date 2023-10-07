from .user import CreateUserDTO, UserDTO, UpdateUserDTO
from .musician import CreateMusicianDTO, MusicianDTO, UpdateMusicianDTO
from .band import (
    CreateBandDTO,
    BandDTO,
    UpdateBandDTO,
    FullBandDTO,
    UpdateMusicianBandDTO,
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
