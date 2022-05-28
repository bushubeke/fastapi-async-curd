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
def test_cleint(testing_client):
    # response =testing_client.post("/test",json=test_item)
    # assert response.status_code == 200
    assert testing_client is not None
def test_table_cleint(testing_client):
    response =testing_client.post("/test",json=test_item)
    print(response.json())
    assert response.status_code == 200
    # assert testing_client is not None

def test_user_route_cleint(testing_client):
    response =testing_client.post("/user",json=antother)
    assert response.status_code != 200
    # assert testing_client is not None