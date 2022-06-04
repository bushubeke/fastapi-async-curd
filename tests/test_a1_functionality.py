import pytest
from httpx import AsyncClient


test_item={
  "ID": 0,
  "UUID_TYPE": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "JSON_TYPE": {
    "id": 0,
    "name": "John Doe",
    "test_list": [
      "string"
    ]
  },
  "JSONB_TYPE": {
    "id": 0,
    "name": "John Doe",
    "test_list": [
      "string"
    ]
  },
  "ARRAY_TYPE": [
    0
  ],
  "ENUM_TYPE": [
    "Zero"
  ],
  "BOOLEAN_TYPE": True,
  "DATE_TIMESTAMP_TYPE": "2022-03-22T11:35:06.703Z"
}
antother={
  "email": "bushu@example.com",
  "username": "someone",
  "first_name": "something",
  "middle_name": "someday",
  "last_name": "someday",
  "password": "test123",
  "active": True
}

@pytest.mark.asyncio
async def test_testing_table_post(testing_client):
            """Test case for testing_table_create_post

            testing_table
            """
            async with AsyncClient(app=testing_client, base_url="http://test") as client:
                login_user_model = {"password":"password","grant_type":"authorization_code","username":"Bushu","token":"none"}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response = await client.post(
                    "/admin/login",
                    headers={},
                    json=login_user_model,
                )
               
            assert response.status_code == 500
