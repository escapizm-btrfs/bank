import pytest 
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select


from app.main import app
from app.models.user_model import UserModel
from app.dependencies.Annotated import SessionDep


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
                "email": "brutdforce@gmail.com",
                "name": "escapizm",
                "password":"321321"
            }
        )

        data = response.json()

        print(data)
        assert response.status_code == 200
        assert data[1]["email"] == "brutdforce@gmail.com"
        assert "id" in data[1]



        error_responce = await ac.post(
            "/auth/registration",
            json = {
                "email": "brutdforce@gmail.com",
                "name": "escapizm",
                "password":"321321"
            }
        )

        assert error_responce.status_code == 400

        
         

        