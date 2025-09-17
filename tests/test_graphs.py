from pathlib import Path
import pytest

from ndtools import graphs


def test_draw_graph_from_data1():
    data_dir = Path("ema-highway/v1/data")   # adjust if relative path differs
    assert data_dir.exists(), f"Data dir not found: {data_dir}"

    out_path = graphs.draw_graph_from_data(
        data_dir,
        output_name="graph.png",
        with_node_labels=True,
        with_edge_labels=True
    )

    # check the file is created
    assert out_path.exists(), f"Graph image not created: {out_path}"
    assert out_path.stat().st_size > 0, "Output image is empty"

    print(f"[ok] Graph created at {out_path.resolve()}")
