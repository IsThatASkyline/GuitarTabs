from guitar_app.infrastructure.db.models import Band, Song, User


class FakeUserRepo:
    def __init__(self, _users=[]):
        self.users = _users

    async def add_user(self, user_dto):
        user = User(telegram_id=user_dto.telegram_id, username=user_dto.username)
        self.users.append(user)
        return user

    async def list_users(self):
        return self.users

    async def get_user(self, id_: int):
        try:
            return self.users[id_ - 1]
        except IndexError:
            return None

    async def delete_user(self, id_: int):
        try:
            return self.users.pop(id_ - 1)
        except IndexError:
            return None


class FakeSongRepo:
    def __init__(self, _songs=[]):
        self.songs = _songs

    async def add_song(self, song_dto):
        song = Song(title=song_dto.title, band_id=song_dto.band_id)
        self.songs.append(song)
        return self.songs.index(song)

    async def list_songs(self):
        return self.songs

    async def get_song(self, id_: int):
        try:
            return self.songs[id_ - 1]
        except IndexError:
            return None

    async def delete_song(self, id_: int):
        try:
            return self.songs.pop(id_ - 1)
        except IndexError:
            return None


class FakeBandRepo:
    def __init__(self, _bands=[]):
        self.bands = _bands

    async def add_band(self, band_dto):
        band = Band(title=band_dto.title)
        self.bands.append(band)
        return band

    async def list_bands(self):
        return self.bands

    async def get_band(self, id_: int):
        try:
            return self.bands[id_ - 1]
        except IndexError:
            return None

    async def delete_band(self, id_: int):
        try:
            return self.bands.pop(id_ - 1)
        except IndexError:
            return None


class FakeAppHolder:
    def __init__(self, band_repo, song_repo, user_repo) -> None:
        self.user_repo = user_repo
        self.band_repo = band_repo
        self.song_repo = song_repo


class FakeUnitOfWork:
    def __init__(self, band_repo=FakeBandRepo(), song_repo=FakeSongRepo(), user_repo=FakeUserRepo()):
        self.app_holder = FakeAppHolder(band_repo, song_repo, user_repo)
        self.committed = False

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        pass

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass

