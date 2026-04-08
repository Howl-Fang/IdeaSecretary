from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_library_and_idea_flow() -> None:
    create_lib = client.post("/api/libraries", json={"name": "test-lib", "description": "for test"})
    if create_lib.status_code == 409:
        libs = client.get("/api/libraries").json()
        lib = next(x for x in libs if x["name"] == "test-lib")
        lib_id = lib["id"]
    else:
        assert create_lib.status_code == 200
        lib_id = create_lib.json()["id"]

    create_idea = client.post(
        "/api/ideas",
        json={
            "library_id": lib_id,
            "title": "An instant thought",
            "content": "What if we support idea branching with AI notes?",
            "source_type": "text",
            "source_value": "pytest",
        },
    )
    assert create_idea.status_code == 200
    idea_id = create_idea.json()["id"]
    assert idea_id

    tree = client.get(f"/api/ideas/library/{lib_id}/tree")
    assert tree.status_code == 200
    assert len(tree.json()) >= 1

    chat = client.post("/api/chat", json={"library_id": lib_id, "question": "branching"})
    assert chat.status_code == 200
    assert "answer" in chat.json()
