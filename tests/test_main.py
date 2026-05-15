import pytest 
from httpx import AsyncClient, ASGITransport


from app.main import app

'''def test_print_routes():
    print("\n--- ДОСТУПНЫЕ ЭНДПОИНТЫ В API ---")
    for route in app.routes:
        print(f"Путь: {route.path} | Методы: {route.methods}")
    print("---------------------------------\n")
    assert False  # Специально роняем тест, чтобы pytest показал print
'''

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

        assert response.status_code == 200
        
        data = response.json()

        #print(data)
        assert data["success"] == True
        #assert "id" in data     

        