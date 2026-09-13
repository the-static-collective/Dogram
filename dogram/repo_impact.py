from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from .impact_receipt import evaluate_impact_receipt

_IGNORED_PARTS = {".git", ".venv", "venv", "__pycache__", "site-packages"}
_PREVIEW_LIMIT = 12


def _python_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.py")
        if not any(part in _IGNORED_PARTS for part in path.relative_to(root).parts)
    )


def _module_name(root: Path, path: Path) -> str:
    parts = list(path.relative_to(root).with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _package_name(root: Path, path: Path, module_name: str) -> str:
    if path.name == "__init__.py":
        return module_name
    return module_name.rpartition(".")[0]


def _relative_base(package: str, level: int, module: str | None) -> str:
    if level == 0:
        return module or ""
    parts = package.split(".") if package else []
    ascend = level - 1
    if ascend > len(parts):
        return ""
    if ascend:
        parts = parts[:-ascend]
    if module:
        parts.extend(module.split("."))
    return ".".join(part for part in parts if part)


def _import_targets(
    tree: ast.AST,
    package: str,
    module_to_path: dict[str, str],
) -> set[str]:
    targets: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                target = module_to_path.get(alias.name)
                if target:
                    targets.add(target)
        elif isinstance(node, ast.ImportFrom):
            base = _relative_base(package, node.level, node.module)
            for alias in node.names:
                candidate = f"{base}.{alias.name}" if base and alias.name != "*" else base
                target = module_to_path.get(candidate) or module_to_path.get(base)
                if target:
                    targets.add(target)
    return targets


def extract_python_dependency_graph(root: str | Path) -> dict[str, Any]:
    root_path = Path(root).resolve()
    files = _python_files(root_path)
    module_to_path = {
        module: path.relative_to(root_path).as_posix()
        for path in files
        if (module := _module_name(root_path, path))
    }
    nodes = sorted(path.relative_to(root_path).as_posix() for path in files)
    edges: set[tuple[str, str]] = set()

    for path in files:
        source = path.relative_to(root_path).as_posix()
        module = _module_name(root_path, path)
        package = _package_name(root_path, path, module)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=source)
        for target in _import_targets(tree, package, module_to_path):
            if target != source:
                edges.add((source, target))

    return {
        "nodes": nodes,
        "edges": [[source, target] for source, target in sorted(edges)],
    }


def build_repo_impact(baseline_root: str | Path, candidate_root: str | Path) -> dict[str, Any]:
    result, _ = evaluate_impact_receipt(
        {
            "baseline": extract_python_dependency_graph(baseline_root),
            "candidate": extract_python_dependency_graph(candidate_root),
        }
    )
    return result


def _preview(values: list[Any]) -> str:
    if not values:
        return "_none_"
    lines = [f"- `{value}`" for value in values[:_PREVIEW_LIMIT]]
    if len(values) > _PREVIEW_LIMIT:
        lines.append(f"- … {len(values) - _PREVIEW_LIMIT} more")
    return "\n".join(lines)


def render_impact_markdown(impact: dict[str, Any]) -> str:
    node_delta = impact["node_delta"]
    edge_delta = impact["edge_delta"]
    reachability_delta = impact["reachability_delta"]
    lines = [
        "### Dogram Impact Receipt",
        "",
        "| Surface | Added / gained | Removed / lost |",
        "| --- | ---: | ---: |",
        f"| Nodes | {len(node_delta['added'])} | {len(node_delta['removed'])} |",
        f"| Edges | {len(edge_delta['added'])} | {len(edge_delta['removed'])} |",
        f"| Reachability pairs | {len(reachability_delta['gained'])} | {len(reachability_delta['lost'])} |",
        "",
        "#### Added nodes",
        _preview(node_delta["added"]),
        "",
        "#### Removed nodes",
        _preview(node_delta["removed"]),
        "",
        "#### Added edges",
        _preview(edge_delta["added"]),
        "",
        "#### Removed edges",
        _preview(edge_delta["removed"]),
        "",
        "> Comparison only: this receipt reports declared structural deltas; it does not decide whether a change is good, causal, evidentiary, or authoritative.",
    ]
    return "\n".join(lines) + "\n"
