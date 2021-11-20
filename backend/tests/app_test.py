from backend import create_app

app = create_app()


def test_index(client):
    response = client.get("/")
    print("404 returned")
    assert response.status_code == 404
