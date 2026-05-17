import pytest 
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select


from app.main import app
from app.models.user_model import UserModel
from app.dependencies.Annotated import SessionDep

'''@pytest.fixture(scope="session")
def event_loop():
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close'''


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
        create_user_response = await ac.post(
            "/auth/registration",
            json={
                "email": "test_login@test.com",
                "name": "test_login",
                "password":"test"
            }
        )

        #data_user = create_user_reponse.json()

        login_response = await ac.post(
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

        data_login = login_response.json()

        print(data_login)
        #Проверка верной формы в логине
        assert login_response.status_code == 200
        #Проверка создания токена в верной форме логина
        assert "access_token" in data_login
        #проверка некорректнйо формы 
        assert uncorrect_password_response.status_code == 401

@pytest.mark.asyncio
async def test_account_created():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as ac:
        #Создание аккаунта что б с его токеном делать запрос на /accounts
        create_user = await ac.post(
            "/auth/registration",
            json={
                "email": "test_login@test.com",
                "name": "test_login",
                "password":"test"
            }
        )

        #Логин с аккаунта выше, что б получить токен
        login_response = await ac.post(
            "/auth/login",
            data={
                "username": "test_login@test.com",
                "password": "test"
            }
        )

        #вытягивается из json() токен что б потом его вставить в заголовок при создании аккаунта
        token = login_response.json()["access_token"]
        print(token)

        acc_create_response = await ac.post(
            "/accounts",
            json={"balance":100},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert acc_create_response.status_code == 200
        




        