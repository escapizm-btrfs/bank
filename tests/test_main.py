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
        acc_create_response_non_token = await ac.post(
            "accounts",
            json={"balance":3421}
        )


        assert acc_create_response.status_code == 200
        
        assert acc_create_response_non_token.status_code == 401

@pytest.mark.asyncio
async def test_transaciton():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as ac:
        
        #Создается первый пользователь, от аккаунтов которых будут происходить транзакции 
        create_user1_response = await ac.post(
            "/auth/registration",
            json={
                "email": "test_login@test.com",
                "name": "test_login",
                "password":"test"
            }
        ) 

        #Создание второго пользователя
        create_user2_response = await ac.post(
            "/auth/registration",
            json={
                "email": "test_login2@test.com",
                "name": "test_login",
                "password":"test"
            }
        ) 

        #login за первого созданного пользователя
        login_response1 = await ac.post(
            "/auth/login",
            data={
                "username": "test_login@test.com",
                "password": "test"
            }
        )

        #login за второго польователя
        login_response2 = await ac.post(
            "/auth/login",
            data={
                "username": "test_login2@test.com",
                "password": "test"
            }
        )

        #запись выданного токена первого пользователя в переменную 
        token1 = login_response1.json()["access_token"]
        print(f"TOKEN1: {token1}")

        #запись токена второго пользователя в переменную
        token2 = login_response2.json()["access_token"]
        print(f"TOKEN2: {token2}")

        #создание аккаунта первому пользователю от выданного токена
        create_account_response1 = await ac.post(
            "/accounts",
            json={
                "balance":100
            },
            headers={"Authorization": f"Bearer {token1}"}
        )

        #Создание аккаунта второму пользователю от второго токена
        create_account_response2 = await ac.post(
            "/accounts",
            json={
                "balance":100
            },
            headers={"Authorization": f"Bearer {token2}"}
        )
        print(f"DATA1: : {create_account_response1.json}")
        print(f"DATA2: : {create_account_response2.json}")
        #получение json первого созданного аккуанта что б получить в дальнейшем его account_number (для переводов)
        account_number_response1 = create_account_response1.json()[1]["account_number"]

        #получение json второго пользователя
        account_number_response2 = create_account_response2.json()[1]["account_number"]

        #Получение json() первого аккаунта
        
        print(f"account_number1: {account_number_response1}")
        
        
        print(f"account_number2: {account_number_response2}")




        #создание транзакции
        valid_create_transaction_response = await ac.post(
            "/transactions",
            json={
                "from_account_number": str(account_number_response1),
                "to_account_number": str(account_number_response2),
                "amount":100,
            },
            headers={"Authorization": f"Bearer {token1}"}
        )

        print(f"TRANSACTION: {valid_create_transaction_response.status_code}")
        print (f"TRANSACTIO JSON {valid_create_transaction_response.json()}")
        """#ОСТАВНОВИЛСЯ ТУТ ТРАНЗАКЦИЯ НЕ ПРОШЛА"""
        #----Проверка списания у первого пользователя
        current_account1_get = await ac.get(
            "/accounts",
            headers={"Authorization": f"Bearer {token1}"}
        )
        current_account1_json = current_account1_get.json()[0]
        print(current_account1_json)
        assert float(current_account1_json["balance"]) < 100
        #----


        #----Проверка получения денег к второму пользователю
        current_account2_get = await ac.get(
            "/accounts",
            headers={"Authorization": f"Bearer {token2}"}
        )
        current_account_json2 = current_account2_get.json()[0]
        assert float(current_account_json2["balance"]) > 100
        #----


        selfish_create_transaction_response = await ac.post(
            "/transactions",
            json={
                "from_account_number": str(account_number_response1),
                "to_account_number": str(account_number_response1),
                "amount":100,
            },
            headers={"Authorization": f"Bearer {token1}"}
        )

        print(account_number_response1)
        print(selfish_create_transaction_response.json())
        assert selfish_create_transaction_response.status_code == 400


        not_enough_create_transaction_response = await ac.post(
            "/transactions",
            json={
                "from_account_number": str(account_number_response1),
                "to_account_number": str(account_number_response2),
                "amount":200,
            },
            headers={"Authorization": f"Bearer {token1}"}
        )

        
        assert not_enough_create_transaction_response.status_code == 400