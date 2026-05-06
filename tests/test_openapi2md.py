from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "openapi2md.py"
SPEC = importlib.util.spec_from_file_location("openapi2md", SCRIPT_PATH)
assert SPEC and SPEC.loader
openapi2md = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(openapi2md)


@pytest.fixture()
def sample_openapi(tmp_path: Path) -> Path:
    spec = {
        "openapi": "3.0.1",
        "info": {
            "title": "Sample API",
            "version": "1.0.0",
            "description": "Test API",
        },
        "paths": {
            "/users": {
                "get": {
                    "tags": ["User"],
                    "summary": "List users\n# Demo",
                    "operationId": "listUsers",
                    "description": "Test API\nwith extra line",
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "Page number\n---",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "OK\n# response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "code": {"type": "integer"},
                                            "msg": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/users/{id}": {
                "delete": {
                    "tags": ["User"],
                    "summary": "Delete user",
                    "operationId": "deleteUser",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "User ID",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "boolean"}
                                }
                            },
                        }
                    },
                }
            },
        },
    }
    path = tmp_path / "sample-openapi.json"
    path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    return path


def test_convert_is_two_lines_per_endpoint_without_tag_headings(sample_openapi: Path) -> None:
    output = openapi2md.convert(str(sample_openapi), by_tag=True)

    lines = output.splitlines()
    assert len(lines) == 4
    assert lines[0].startswith("## GET /users - List users ＃ Demo")
    assert lines[1].startswith("模块: User | operationId: listUsers")
    assert lines[2].startswith("## DELETE /users/{id} - Delete user")
    assert lines[3].startswith("模块: User | operationId: deleteUser")
    assert all(line.strip() for line in lines)
    assert all(not line.startswith("# ") for line in lines)
    assert "---" not in output
    assert output.count("## ") == 2
    assert "Test API with extra line" in output
    assert "请求参数: page(query, integer, 必填, Page number —)" in output
    assert "请求参数: id(path, integer, 必填, User ID)" in output
    assert "响应: 200 OK ＃ response: code(integer, 可选); msg(string, 可选)" in output


def test_convert_writes_flat_txt_output(sample_openapi: Path, tmp_path: Path) -> None:
    output_path = tmp_path / "sample.txt"
    result = openapi2md.convert(str(sample_openapi), output_path=str(output_path))

    assert output_path.read_text(encoding="utf-8") == result
    assert output_path.suffix == ".txt"
    assert output_path.read_text(encoding="utf-8").count("## ") == 2
    assert output_path.read_text(encoding="utf-8").splitlines()[0].startswith("## ")
