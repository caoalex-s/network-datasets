from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import glob

try:
    from jsonschema import validate
except ImportError:
    print("Please install jsonschema: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

def load_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to parse JSON: {p} ({e})") from e

def validate_dataset(root: Path, dataset_path: str, schemas_dir: Path) -> list[str]:
    """Validate nodes/edges/probs for a single dataset. Returns list of problems."""
    problems: list[str] = []
    ds_root = (root / dataset_path).resolve()

    nodes_p = ds_root / "data" / "nodes.json"
    edges_p = ds_root / "data" / "edges.json"
    probs_p = ds_root / "data" / "probs.json"

    nodes_schema = load_json(schemas_dir / "nodes.schema.json")
    edges_schema = load_json(schemas_dir / "edges.schema.json")
    probs_schema = load_json(schemas_dir / "probs.schema.json")

    # nodes.json
    try:
        nodes = load_json(nodes_p)
        validate(nodes, nodes_schema)
    except FileNotFoundError:
        problems.append(f"Missing: {nodes_p}")
    except Exception as e:
        problems.append(f"nodes.json invalid: {e}")

    # edges.json
    try:
        edges = load_json(edges_p)
        validate(edges, edges_schema)
    except FileNotFoundError:
        problems.append(f"Missing: {edges_p}")
    except Exception as e:
        problems.append(f"edges.json invalid: {e}")

    # probs.json (allow variants like probs_*.json)
    probs_candidates = list((ds_root / "data").glob("probs*.json"))

    if not probs_candidates:
        problems.append(f"Missing: no probs*.json found in {ds_root/'data'}")
    else:
        for probs_p in probs_candidates:
            try:
                probs = load_json(probs_p)
                validate(probs, probs_schema)
            except Exception as e:
                problems.append(f"{probs_p.name} invalid: {e}")

        return problems

def main():
    ap = argparse.ArgumentParser(description="Validate datasets against JSON Schemas.")
    ap.add_argument("--root", type=Path, default=Path("."), help="Repo root containing registry.json and schema/")
    ap.add_argument("--dataset", type=str, default=None,
                    help="Optional dataset name to validate (matches 'name' in registry.json).")
    args = ap.parse_args()

    root = args.root.resolve()
    reg_path = root / "registry.json"
    schema_dir = root / "schema"

    if not reg_path.exists():
        print(f"registry.json not found at {reg_path}", file=sys.stderr)
        sys.exit(2)
    if not schema_dir.exists():
        print(f"schema/ not found at {schema_dir}", file=sys.stderr)
        sys.exit(2)

    registry = load_json(reg_path)

    entries = registry
    if args.dataset:
        entries = [r for r in registry if r.get("name") == args.dataset]
        if not entries:
            print(f"No dataset named '{args.dataset}' in registry.json", file=sys.stderr)
            sys.exit(3)

    any_errors = False
    for rec in entries:
        name = rec.get("name")
        path = rec.get("path")
        print(f"Validating: {name} @ {path}")
        problems = validate_dataset(root, path, schema_dir)
        if problems:
            any_errors = True
            for msg in problems:
                print(f"  - {msg}")
        else:
            print("  ✓ OK")

    sys.exit(1 if any_errors else 0)

if __name__ == "__main__":
    main()
