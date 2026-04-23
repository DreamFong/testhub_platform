"""
将 OpenAPI JSON 转换为 RAGFlow 友好的 Markdown 文档。
每个 API 接口生成一个扁平段落（单层标题），避免被 RAGFlow book 分块切碎。

用法:
    python openapi2md.py <input.json> [-o output.md] [--by-tag]
"""
import argparse
import json
import sys
from typing import Any


def resolve_ref(spec: dict, ref: str) -> dict:
    if not ref.startswith("#/"):
        return {"type": "string", "description": f"(unresolved ref: {ref})"}
    parts = ref.lstrip("#/").split("/")
    node: Any = spec
    for p in parts:
        node = node.get(p, {})
    return node if isinstance(node, dict) else {}


def format_schema_inline(spec: dict, root: dict, depth: int = 0, max_depth: int = 2) -> str:
    """将 JSON Schema 转为单行内联格式，避免产生换行导致分块碎片化。"""
    if depth > max_depth:
        return "..."
    if "$ref" in spec:
        spec = resolve_ref(root, spec["$ref"])

    schema_type = spec.get("type", "object")
    desc = spec.get("description", "")
    example = spec.get("example", "")

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
            p_desc = prop.get("description", "")
            p_example = prop.get("example", "")
            req = "必填" if name in required_fields else "可选"
            s = f"{name}({p_type}, {req}"
            if p_desc:
                s += f", {p_desc}"
            if p_example:
                s += f", 示例:{p_example}"
            s += ")"
            parts.append(s)
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


def format_params_inline(params: list[dict]) -> str:
    if not params:
        return ""
    parts = []
    for p in params:
        name = p.get("name", "")
        location = p.get("in", "")
        p_type = p.get("schema", {}).get("type", "string")
        required = "必填" if p.get("required") else "可选"
        desc = p.get("description", "")
        example = p.get("example", "")
        s = f"{name}({location}, {p_type}, {required}"
        if desc:
            s += f", {desc}"
        if example:
            s += f", 示例:{example}"
        s += ")"
        parts.append(s)
    return "; ".join(parts)


def convert_endpoint(path: str, method: str, spec: dict, root: dict) -> str:
    """将单个 API 端点转为一个扁平的 Markdown 段落，全部内容在一个 ## 标题下。"""
    lines = []
    tag = spec.get("tags", ["未分类"])[0]
    summary = spec.get("summary", "")
    description = spec.get("description", "")
    operation_id = spec.get("operationId", "")

    # 唯一标题：方法 + 路径 + 摘要
    title = f"{method.upper()} {path}"
    if summary:
        title += f" - {summary}"
    lines.append(f"## {title}")
    lines.append("")

    # 元信息行
    meta = [f"模块: {tag}", f"operationId: {operation_id}"]
    lines.append(" | ".join(meta))
    lines.append("")

    if description:
        lines.append(description)
        lines.append("")

    # 请求参数（query/path/header）
    params = spec.get("parameters", [])
    if params:
        lines.append(f"请求参数: {format_params_inline(params)}")
        lines.append("")

    # 请求体
    request_body = spec.get("requestBody", {})
    if request_body:
        content = request_body.get("content", {})
        for ct, ct_spec in content.items():
            schema = ct_spec.get("schema", {})
            required = "必填" if request_body.get("required") else "可选"
            schema_str = format_schema_inline(schema, root)
            lines.append(f"请求体({ct}, {required}): {schema_str}")
            lines.append("")

    # 响应
    responses = spec.get("responses", {})
    if responses:
        resp_parts = []
        for code, resp_spec in responses.items():
            resp_desc = resp_spec.get("description", "")
            resp_content = resp_spec.get("content", {})
            for ct, ct_spec in resp_content.items():
                schema = ct_spec.get("schema", {})
                schema_str = format_schema_inline(schema, root)
                resp_parts.append(f"{code} {resp_desc}: {schema_str}")
        if resp_parts:
            lines.append("响应: " + " | ".join(resp_parts))
            lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def convert(input_path: str, output_path: str | None = None, by_tag: bool = False) -> str:
    with open(input_path, encoding="utf-8") as f:
        spec = json.load(f)

    info = spec.get("info", {})
    paths = spec.get("paths", {})

    all_sections: list[tuple[str, str]] = []

    for path, methods in paths.items():
        for method, endpoint_spec in methods.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            tag = endpoint_spec.get("tags", ["未分类"])[0]
            md = convert_endpoint(path, method, endpoint_spec, spec)
            all_sections.append((tag, md))

    if by_tag:
        from collections import OrderedDict
        grouped: dict[str, list[str]] = OrderedDict()
        for tag, md in all_sections:
            grouped.setdefault(tag, []).append(md)

        parts = [
            f"# {info.get('title', 'API Documentation')}",
            f"版本: {info.get('version', '')} | 描述: {info.get('description', '')} | 接口总数: {len(all_sections)}",
            "",
        ]
        for tag, mds in grouped.items():
            parts.append(f"# {tag}")
            parts.append("")
            parts.extend(mds)
        output = "\n".join(parts)
    else:
        header = [
            f"# {info.get('title', 'API Documentation')}",
            f"版本: {info.get('version', '')} | 描述: {info.get('description', '')} | 接口总数: {len(all_sections)}",
            "",
        ]
        output = "\n".join(header + [md for _, md in all_sections])

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)
    return output


def main():
    parser = argparse.ArgumentParser(description="将 OpenAPI JSON 转为 RAGFlow 友好的 Markdown（扁平格式）")
    parser.add_argument("input", help="OpenAPI JSON 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--by-tag", action="store_true", help="按模块标签分组")
    args = parser.parse_args()
    result = convert(args.input, args.output, args.by_tag)
    if not args.output:
        print(result)
    else:
        count = result.count("## ")
        print(f"已转换 {count} 个接口 -> {args.output}")


if __name__ == "__main__":
    main()
