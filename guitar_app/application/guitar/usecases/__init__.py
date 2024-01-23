from .user import GetUsers, UpdateUser, CreateUser, DeleteUser, GetUserById
from .band import (
    GetBands,
    UpdateBand,
    CreateBand,
    DeleteBand,
    GetBandById,
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
    HitSong,
    GetTabsForSong,
    GetTabById,
    DeleteTabs,
)
