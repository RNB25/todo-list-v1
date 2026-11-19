import uuid6
from fastapi import status


def test_tc001_create_valid_todo_title_only(client):
    res = client.post("/api/v1/todos", json={"title": "Belajar FastAPI"})
    assert res.status_code == status.HTTP_201_CREATED
    data = res.json()["data"]
    assert data["title"] == "Belajar FastAPI"
    assert data["status"] == "pending"
    assert data["priority"] == "medium"
    assert data["description"] is None
    assert len(data["id"]) == 36
    # Verify UUID v7
    u = uuid6.UUID(data["id"])
    assert u.version == 7


def test_tc002_create_title_kosong(client):
    res = client.post("/api/v1/todos", json={"title": "   "})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    err = res.json()["error"]
    assert err["code"] == "VALIDATION_ERROR"


def test_tc003_create_title_256_karakter(client):
    res = client.post("/api/v1/todos", json={"title": "A" * 256})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    err = res.json()["error"]
    assert err["code"] == "VALIDATION_ERROR"


def test_tc004_create_status_valid(client):
    for s in ["pending", "progress", "done"]:
        res = client.post("/api/v1/todos", json={"title": f"Tugas {s}", "status": s})
        assert res.status_code == status.HTTP_201_CREATED
        assert res.json()["data"]["status"] == s


def test_tc005_create_status_tidak_valid(client):
    res = client.post("/api/v1/todos", json={"title": "Tugas", "status": "blocked"})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"


def test_tc006_create_priority_valid(client):
    for p in ["low", "medium", "high"]:
        res = client.post("/api/v1/todos", json={"title": f"Tugas {p}", "priority": p})
        assert res.status_code == status.HTTP_201_CREATED
        assert res.json()["data"]["priority"] == p


def test_tc007_create_priority_tidak_valid(client):
    res = client.post("/api/v1/todos", json={"title": "Tugas", "priority": "urgent"})
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"


def test_tc008_description_null_or_omitted(client):
    res1 = client.post("/api/v1/todos", json={"title": "Tugas Tanpa Deskripsi"})
    assert res1.status_code == status.HTTP_201_CREATED
    assert res1.json()["data"]["description"] is None

    res2 = client.post("/api/v1/todos", json={"title": "Tugas Deskripsi Null", "description": None})
    assert res2.status_code == status.HTTP_201_CREATED
    assert res2.json()["data"]["description"] is None


def test_tc009_validasi_timestamp(client):
    res = client.post("/api/v1/todos", json={"title": "Tugas Cek Waktu"})
    assert res.status_code == status.HTTP_201_CREATED
    data = res.json()["data"]
    assert data["created_at"].endswith("Z")
    assert data["updated_at"].endswith("Z")


def test_tc010_tc011_tc012_tc013_list_filters(client):
    # Seed specific test data from SRS Section 11.2
    client.post("/api/v1/todos", json={"title": "Belajar FastAPI", "status": "pending", "priority": "low"})
    client.post("/api/v1/todos", json={"title": "Mengerjakan UI Vue", "status": "progress", "priority": "medium"})
    client.post("/api/v1/todos", json={"title": "Review dokumentasi", "status": "done", "priority": "high"})
    client.post("/api/v1/todos", json={"title": "Laporan sprint", "status": "pending", "priority": "high"})

    # TC-010: List todos
    res = client.get("/api/v1/todos")
    assert res.status_code == status.HTTP_200_OK
    assert "data" in res.json()
    assert "meta" in res.json()

    # TC-011: Filter status done
    res_done = client.get("/api/v1/todos?status=done")
    assert res_done.status_code == status.HTTP_200_OK
    for item in res_done.json()["data"]:
        assert item["status"] == "done"

    # TC-012: Filter priority high
    res_high = client.get("/api/v1/todos?priority=high")
    assert res_high.status_code == status.HTTP_200_OK
    for item in res_high.json()["data"]:
        assert item["priority"] == "high"

    # TC-013: Keyword search
    res_q = client.get("/api/v1/todos?q=Laporan")
    assert res_q.status_code == status.HTTP_200_OK
    assert any("Laporan" in item["title"] for item in res_q.json()["data"])


def test_tc014_tc015_sorting(client):
    # TC-014: Sort asc and desc
    res_asc = client.get("/api/v1/todos?sort_by=title&sort_order=asc")
    assert res_asc.status_code == status.HTTP_200_OK

    res_desc = client.get("/api/v1/todos?sort_by=title&sort_order=desc")
    assert res_desc.status_code == status.HTTP_200_OK

    # TC-015: Sort not in allowlist
    res_inv = client.get("/api/v1/todos?sort_by=secret_column")
    assert res_inv.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert res_inv.json()["error"]["code"] == "VALIDATION_ERROR"


def test_tc016_tc017_tc018_pagination(client):
    # TC-016: First page, page_size=2
    res = client.get("/api/v1/todos?page=1&page_size=2")
    assert res.status_code == status.HTTP_200_OK
    meta = res.json()["meta"]
    assert meta["page"] == 1
    assert meta["page_size"] == 2
    assert len(res.json()["data"]) <= 2

    # TC-017: Out of bounds pagination
    res_zero = client.get("/api/v1/todos?page=0")
    assert res_zero.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    res_huge_size = client.get("/api/v1/todos?page_size=101")
    assert res_huge_size.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # TC-018: Page > total_pages returns empty data with consistent meta
    res_big_page = client.get("/api/v1/todos?page=9999&page_size=20")
    assert res_big_page.status_code == status.HTTP_200_OK
    assert res_big_page.json()["data"] == []
    assert res_big_page.json()["meta"]["page"] == 9999


def test_tc019_tc020_tc021_detail(client):
    # Create item
    create_res = client.post("/api/v1/todos", json={"title": "Detail Todo"})
    todo_id = create_res.json()["data"]["id"]

    # TC-019: Get valid detail
    res = client.get(f"/api/v1/todos/{todo_id}")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["data"]["id"] == todo_id

    # TC-020: UUID valid but not found
    random_uuid = str(uuid6.uuid7())
    res_not_found = client.get(f"/api/v1/todos/{random_uuid}")
    assert res_not_found.status_code == status.HTTP_404_NOT_FOUND
    assert res_not_found.json()["error"]["code"] == "TODO_NOT_FOUND"

    # TC-021: Invalid UUID format
    res_invalid_format = client.get("/api/v1/todos/not-a-uuid")
    assert res_invalid_format.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert res_invalid_format.json()["error"]["code"] == "VALIDATION_ERROR"


def test_tc022_tc023_patch_update(client):
    create_res = client.post("/api/v1/todos", json={"title": "Todo to update", "status": "pending"})
    todo_id = create_res.json()["data"]["id"]
    original_created_at = create_res.json()["data"]["created_at"]

    # TC-022: Update status
    res = client.patch(f"/api/v1/todos/{todo_id}", json={"status": "done"})
    assert res.status_code == status.HTTP_200_OK
    updated_data = res.json()["data"]
    assert updated_data["status"] == "done"
    assert updated_data["created_at"] == original_created_at

    # TC-023: Empty body rejected
    res_empty = client.patch(f"/api/v1/todos/{todo_id}", json={})
    assert res_empty.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_tc024_tc025_delete(client):
    create_res = client.post("/api/v1/todos", json={"title": "Todo to delete"})
    todo_id = create_res.json()["data"]["id"]

    # TC-024: Delete valid record
    res_del = client.delete(f"/api/v1/todos/{todo_id}")
    assert res_del.status_code == status.HTTP_204_NO_CONTENT

    # Verify not found now
    res_get = client.get(f"/api/v1/todos/{todo_id}")
    assert res_get.status_code == status.HTTP_404_NOT_FOUND

    # TC-025: Delete non-existing record
    random_uuid = str(uuid6.uuid7())
    res_del_missing = client.delete(f"/api/v1/todos/{random_uuid}")
    assert res_del_missing.status_code == status.HTTP_404_NOT_FOUND


def test_tc026_tc027_tc028_bulk_random(client):
    # TC-027: Bulk generate count=1
    res1 = client.post("/api/v1/todos/bulk-random", json={"count": 1})
    assert res1.status_code == status.HTTP_201_CREATED
    assert res1.json()["data"]["created_count"] == 1

    # TC-028: Bulk generate count=1001 (beyond max 1000)
    res_excess = client.post("/api/v1/todos/bulk-random", json={"count": 1001})
    assert res_excess.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # TC-026: Bulk generate default (count=1000)
    res_default = client.post("/api/v1/todos/bulk-random", json={})
    assert res_default.status_code == status.HTTP_201_CREATED
    assert res_default.json()["data"]["requested_count"] == 1000
    assert res_default.json()["data"]["created_count"] == 1000


def test_health_check(client):
    res = client.get("/api/v1/health")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["status"] == "healthy"
