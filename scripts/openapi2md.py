"""
将 OpenAPI JSON 转换为 RAGFlow 友好的 Markdown 文档。
每个 API 接口输出为两行扁平段落，避免被 RAGFlow book 分块切碎。

用法:
    python openapi2md.py <input.json> [-o output.txt] [--by-tag]
"""

import argparse
import json
import re
import sys
from typing import Any


def normalize_inline_text(value: Any) -> str:
    text = " ".join(str(value).split())
    text = text.replace("|", "｜")
    text = text.replace("#", "＃")
    text = text.replace("---", "—")
    text = re.sub(r"^\s*＃{1,6}\s*", "", text)
    return text.strip()


def resolve_ref(spec: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        return {"type": "string", "description": f"(unresolved ref: {ref})"}
    parts = ref.lstrip("#/").split("/")
    node: Any = spec
    for part in parts:
        node = node.get(part, {})
    return node if isinstance(node, dict) else {}


def format_schema_inline(
    spec: dict[str, Any], root: dict[str, Any], depth: int = 0, max_depth: int = 2
) -> str:
    """将 JSON Schema 转为单行内联格式，避免产生换行导致分块碎片化。"""
    if depth > max_depth:
        return "..."
    if "$ref" in spec:
        spec = resolve_ref(root, spec["$ref"])

    schema_type = spec.get("type", "object")
    desc = normalize_inline_text(spec.get("description", ""))
    example = normalize_inline_text(spec.get("example", ""))

    if schema_type == "array":
        items = spec.get("items", {})
        item_str = format_schema_inline(items, root, depth + 1, max_depth)
        base = f"array<{item_str}>"
        if desc:
            base += f" ({desc})"
        return base

    if schema_type == "object":
        props = spec.get("properties", {})
        if not props:
            base = "object"
            if desc:
                base += f" ({desc})"
            return base

        required_fields = set(spec.get("required", []))
        parts = []
        for name, prop in props.items():
            prop = dict(prop)
            if "$ref" in prop:
                prop.update(resolve_ref(root, prop.pop("$ref")))
            p_type = prop.get("type", "string")
            p_desc = normalize_inline_text(prop.get("description", ""))
            p_example = normalize_inline_text(prop.get("example", ""))
            req = "必填" if name in required_fields else "可选"
            item = f"{name}({p_type}, {req}"
            if p_desc:
                item += f", {p_desc}"
            if p_example:
                item += f", 示例:{p_example}"
            item += ")"
            parts.append(item)
        return "; ".join(parts)

    result = schema_type
    fmt = spec.get("format", "")
    if fmt:
        result += f"({fmt})"
    if desc:
        result += f" ({desc})"
    if example:
        result += f" 示例:{example}"
    enum_vals = spec.get("enum", [])
    if enum_vals:
        result += f" 枚举:{enum_vals}"
    return result


def format_params_inline(params: list[dict[str, Any]]) -> str:
    if not params:
        return ""
    parts = []
    for param in params:
        name = normalize_inline_text(param.get("name", ""))
        location = normalize_inline_text(param.get("in", ""))
        p_type = normalize_inline_text(param.get("schema", {}).get("type", "string"))
        required = "必填" if param.get("required") else "可选"
        desc = normalize_inline_text(param.get("description", ""))
        example = normalize_inline_text(param.get("example", ""))
        item = f"{name}({location}, {p_type}, {required}"
        if desc:
            item += f", {desc}"
        if example:
            item += f", 示例:{example}"
        item += ")"
        parts.append(item)
    return "; ".join(parts)


def convert_endpoint(path: str, method: str, spec: dict[str, Any], root: dict[str, Any]) -> str:
    """将单个 API 端点转为一个两行 Markdown 段落。"""
    tag = normalize_inline_text(spec.get("tags", ["未分类"])[0])
    summary = normalize_inline_text(spec.get("summary", ""))
    description = normalize_inline_text(spec.get("description", ""))
    operation_id = normalize_inline_text(spec.get("operationId", ""))

    title = f"## {method.upper()} {path}"
    if summary:
        title += f" - {summary}"

    body_parts = [f"模块: {tag}", f"operationId: {operation_id}"]

    if description:
        body_parts.append(description)

    params = spec.get("parameters", [])
    if params:
        body_parts.append(f"请求参数: {format_params_inline(params)}")

    request_body = spec.get("requestBody", {})
    if request_body:
        content = request_body.get("content", {})
        body_parts.extend(
            [
                f"请求体({normalize_inline_text(content_type)}, {'必填' if request_body.get('required') else '可选'}): {format_schema_inline(content_spec.get('schema', {}), root)}"
                for content_type, content_spec in content.items()
            ]
        )

    responses = spec.get("responses", {})
    if responses:
        resp_parts = []
        for code, resp_spec in responses.items():
            resp_desc = normalize_inline_text(resp_spec.get("description", ""))
            resp_content = resp_spec.get("content", {})
            for content_type, content_spec in resp_content.items():
                schema = content_spec.get("schema", {})
                schema_str = format_schema_inline(schema, root)
                if resp_desc:
                    resp_parts.append(f"{code} {resp_desc}: {schema_str}")
                else:
                    resp_parts.append(f"{code}: {schema_str}")
        if resp_parts:
            body_parts.append("响应: " + " | ".join(resp_parts))

    return "\n".join([title, " | ".join(part for part in body_parts if part)])


def convert(input_path: str, output_path: str | None = None, by_tag: bool = False) -> str:
    with open(input_path, encoding="utf-8") as f:
        spec = json.load(f)

    paths = spec.get("paths", {})

    all_sections: list[tuple[str, str, str, str, str]] = []

    for path, methods in paths.items():
        for method, endpoint_spec in methods.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            tag = normalize_inline_text(endpoint_spec.get("tags", ["未分类"])[0])
            summary = normalize_inline_text(endpoint_spec.get("summary", ""))
            md = convert_endpoint(path, method, endpoint_spec, spec)
            all_sections.append((tag, path, method, summary, md))

    if by_tag:
        all_sections.sort(key=lambda item: (item[0], item[1], item[2], item[3]))

    output = "\n".join(md for _, _, _, _, md in all_sections)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="将 OpenAPI JSON 转为 RAGFlow 友好的 Markdown（扁平格式）")
    parser.add_argument("input", help="OpenAPI JSON 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--by-tag", action="store_true", help="按模块标签排序输出")
    args = parser.parse_args()
    result = convert(args.input, args.output, args.by_tag)
    if not args.output:
        print(result)
    else:
        count = result.count("## ")
        print(f"已转换 {count} 个接口 -> {args.output}")


if __name__ == "__main__":
    main()
