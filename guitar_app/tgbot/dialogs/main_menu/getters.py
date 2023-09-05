from guitar_app.application.guitar import dto


async def get_main(user: dto.UserDTO, **_):
    return {
        'user': user,
    }
