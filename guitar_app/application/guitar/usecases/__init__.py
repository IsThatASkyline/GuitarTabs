from .user import GetUsers, UpdateUser, CreateUser, DeleteUser, GetUserById
from .musician import (
    GetMusicians,
    UpdateMusician,
    CreateMusician,
    DeleteMusician,
    GetMusicianById,
)
from .band import (
    GetBands,
    UpdateBand,
    CreateBand,
    DeleteBand,
    GetBandById,
    UpdateMusicianBand,
)
from .song import (
    GetSongs,
    UpdateSong,
    CreateSong,
    DeleteSong,
    GetSongById,
    GetSongsByGroup,
    AddSongToFavorite,
    RemoveSongFromFavorite,
    GetFavoriteSongsByUser,
    GetModulatedSong,
    FindSong,
)
