import pytest 
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select


from app.main import app
from app.models.user_model import UserModel
from app.dependencies.Annotated import SessionDep

@pytest.fixture(scope="session")
def event_loop():
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close


@pytest.mark.asyncio
async def test_registration():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/auth/registration",
            json={
                "email": "test_reg@test.com",
                "name": "test_reg",
                "password":"test"
            }
        )
        data = response.json()
        print(data)

        assert response.status_code == 200
        assert data[1]["email"] == "test_reg@test.com"
        assert "id" in data[1]



        error_responce = await ac.post(
            "/auth/registration",
            json = {
                "email": "test_reg@test.com",
                "name": "test_reg",
                "password":"test"
            }
        )
        assert error_responce.status_code == 400

        
         
@pytest.mark.asyncio
async def test_login():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        create_user = await ac.post(
            "/auth/registration",
            json={
                "email": "test_login@test.com",
                "name": "test_login",
                "password":"test"
            }
        )

        #data_user = create_user.json()

        response = await ac.post(
            "/auth/login",
            data={
                "username": "test_login@test.com",
                "password": "test"
            }
        )

        uncorrect_password_response = await ac.post(
            "/auth/login",
            data={
                "username":"test_login@test.com",
                "password":"test1"
            }
        )

        data_login = response.json()

        print(data_login)
        #Проверка верной формы в логине
        assert response.status_code == 200
        #Проверка создания токена в верной форме логина
        assert "access_token" in data_login
        #проверка некорректнйо формы 
        assert uncorrect_password_response.status_code == 401







        