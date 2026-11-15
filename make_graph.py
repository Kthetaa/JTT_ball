import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import os
# GitHub Actions以外でのみGUIを使用
if os.environ.get("GITHUB_ACTIONS") != "true":
    import tkinter as tk
    from tkinter import ttk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pydot

BASE_DIR = Path(__file__).resolve().parent

def load_graph(filename):
    G = nx.DiGraph()

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # 空行・コメント行を無視
            if not line or line.startswith("#"):
                continue

            # 頂点と隣接頂点に分割
            if ":" not in line:
                raise ValueError(f"形式が不正です: {line}")

            vertex, neighbors = line.split(":", 1)
            vertex = vertex.strip()

            if not vertex:
                raise ValueError(f"頂点名がありません: {line}")

            G.add_node(vertex)

            for neighbor in neighbors.split():
                G.add_edge(vertex, neighbor)
    
    return G

def draw_graph(G):
    if not nx.is_directed_acyclic_graph(G):
        print("このグラフは非循環有向グラフではありません。")
        print("閉路:", nx.find_cycle(G))
        return

    print("非循環有向グラフです。")

    # Graphvizによる配置
    A = nx.nx_pydot.to_pydot(G)

    A.set_rankdir("TB")
    A.set_ranksep("1.0")
    A.set_nodesep("2.0")

    # Graphvizで配置計算
    dot_data = A.create_dot(prog="dot").decode("utf-8")

    # 計算結果を再読み込み
    A2 = pydot.graph_from_dot_data(dot_data)[0]

    # 座標を取得
    pos = {}

    for node in A2.get_nodes():
        name = node.get_name().strip('"')

        if name in G.nodes:
            p = node.get_pos()

            if p:
                x, y = map(float, p.strip('"').rstrip("!").split(","))
                pos[name] = (x, y)

    # 画面表示の設定
    if os.environ.get("GITHUB_ACTIONS") != "true":
    # ウィンドウ
        root = tk.Tk()
        root.title("DAG Viewer")
        root.geometry("1000x700")

        # スクロール可能な領域
        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        scrollbar_y = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=canvas.yview
        )
        scrollbar_x = ttk.Scrollbar(
            frame, orient=tk.HORIZONTAL, command=canvas.xview
        )

        canvas.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # マウスホイールによる上下スクロール
        def on_mousewheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        # Shift + マウスホイールで左右スクロール
        def on_shift_mousewheel(event):
            canvas.xview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)


    # グラフの描画設定（常に実行）
    xs = [x for x, y in pos.values()]
    ys = [y for x, y in pos.values()]

    width = max(xs) - min(xs)
    height = max(ys) - min(ys)

    scale = 100
    fig_width = max(8, width / scale + 2)
    fig_height = max(8, height / scale + 2)

    fig = Figure(figsize=(fig_width, fig_height), dpi=100)
    ax = fig.add_subplot(111)

    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color="lightblue",
        node_size=1500,
        font_size=12,
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0"
    )

    ax.set_aspect("equal")

    ax.set_xlim(min(xs) - 100, max(xs) + 100)
    ax.set_ylim(min(ys) - 100, max(ys) + 100)

    ax.axis("off")
    fig.tight_layout()

    # 画像は常に保存
    fig.savefig(BASE_DIR / "graph.png", dpi=300, bbox_inches="tight")


    # 画面表示
    if os.environ.get("GITHUB_ACTIONS") != "true":
        # MatplotlibをTkinterに埋め込む
        graph_widget = FigureCanvasTkAgg(fig, master=canvas)
        graph_widget.draw()

        widget = graph_widget.get_tk_widget()
        canvas.create_window(0, 0, anchor="nw", window=widget)

        # スクロール範囲を設定
        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        widget.bind("<Configure>", update_scroll_region)

        root.mainloop()


if __name__ == "__main__":
    graph_path = Path(__file__).parent / "graph.txt"
    G = load_graph(graph_path)
    draw_graph(G)
