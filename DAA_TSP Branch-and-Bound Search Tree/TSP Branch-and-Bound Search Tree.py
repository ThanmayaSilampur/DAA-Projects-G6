"""Project 14: TSP using Branch and Bound (reduced cost matrix) + step-by-step visualization."""
import heapq, itertools
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.animation import PillowWriter

INF = float("inf")
CITIES = ["A", "B", "C", "D"]
COST = [[INF, 10, 15, 20],
        [10, INF, 35, 25],
        [15, 35, INF, 30],
        [20, 25, 30, INF]]
COLORS = {"expanded": "#cfe3ff", "pruned": "#ffb3b3", "optimal": "#a8e6a1",
          "feasible_worse": "#ffe0a3", "open": "#eeeeee"}
name = lambda p: "→".join(CITIES[x] for x in p)


def reduce_matrix(m):
    """Row- then column-reduce m in place; return total reduction."""
    n, total = len(m), 0
    for i in range(n):
        r = min(m[i])
        if 0 < r < INF:
            total += r
            m[i] = [x - r for x in m[i]]
    for j in range(n):
        c = min(m[i][j] for i in range(n))
        if 0 < c < INF:
            total += c
            for i in range(n):
                m[i][j] -= c
    return total


def solve():
    n = len(COST)
    m0 = [row[:] for row in COST]
    root_bound = reduce_matrix(m0)
    nodes = [{"id": 0, "parent": None, "path": [0], "bound": root_bound,
              "edge": None, "red": root_bound}]
    status = {0: "open"}
    log = [({0}, dict(status), f"Step 0: root A, reduce cost matrix → LB = {root_bound}")]
    counter = itertools.count(1)
    heap = [(root_bound, 0, 0, m0)]
    best, best_id, step = INF, None, 0
    while heap:
        bound, _, nid, mat = heapq.heappop(heap)
        node = nodes[nid]
        step += 1
        if bound >= best:
            status[nid] = "pruned"
            log.append((set(status), dict(status),
                        f"Step {step}: pop {name(node['path'])} (LB={bound} ≥ best {best}) → PRUNED"))
            continue
        status[nid] = "expanded"
        path, i = node["path"], node["path"][-1]
        for j in range(n):
            if j in path:
                continue
            m = [row[:] for row in mat]
            edge = m[i][j]
            for k in range(n):
                m[i][k] = INF
                m[k][j] = INF
            m[j][0] = INF
            red = reduce_matrix(m)
            cost = bound + edge + red
            cid = next(counter)
            nodes.append({"id": cid, "parent": nid, "path": path + [j], "bound": cost,
                          "edge": edge, "red": red})
            if len(path) + 1 == n:
                status[cid] = "optimal" if cost < best else "feasible_worse"
                if cost < best:
                    if best_id is not None:
                        status[best_id] = "feasible_worse"
                    best, best_id = cost, cid
            else:
                status[cid] = "open"
                heapq.heappush(heap, (cost, cid, cid, m))
        kids = [c for c in nodes if c["parent"] == nid]
        txt = ", ".join(f"{name(c['path'])}={c['bound']}" for c in kids)
        extra = f"  |  complete tour found, best = {best}" if len(path) + 1 == n else ""
        log.append((set(status), dict(status), f"Step {step}: expand {name(path)} (LB={bound}) → {txt}{extra}"))
    return nodes, best, best_id, log


def layout(nodes):
    levels = {}
    for nd in nodes:
        levels.setdefault(len(nd["path"]) - 1, []).append(nd)
    pos = {}
    for lv, lst in sorted(levels.items()):
        if lv > 0:
            lst.sort(key=lambda d: (pos[d["parent"]][0], d["id"]))
        for k, nd in enumerate(lst):
            pos[nd["id"]] = ((k + 1) / (len(lst) + 1) * 16, -lv * 3)
    return pos


def draw(ax, nodes, pos, visible, status, title):
    ax.clear()
    for nd in nodes:
        if nd["parent"] is not None and nd["id"] in visible:
            (x1, y1), (x2, y2) = pos[nd["parent"]], pos[nd["id"]]
            ax.plot([x1, x2], [y1, y2], color="#555", lw=1, zorder=1)
    for nd in nodes:
        if nd["id"] not in visible:
            continue
        x, y = pos[nd["id"]]
        st = status[nd["id"]]
        path = nd["path"] + ([0] if st in ("optimal", "feasible_worse") else [])
        txt = f"{name(path)}\nLB = {nd['bound']}" + ("\n(pruned)" if st == "pruned" else "")
        ax.text(x, y, txt, ha="center", va="center", fontsize=9, zorder=2,
                bbox=dict(boxstyle="round,pad=0.4", fc=COLORS[st],
                          ec="green" if st == "optimal" else "#333", lw=2.5 if st == "optimal" else 1))
    ax.set_xlim(0, 16); ax.set_ylim(-9.8, 1)
    ax.legend(handles=[Patch(fc=COLORS["open"], ec="#333", label="Generated (waiting in queue)"),
                       Patch(fc=COLORS["expanded"], ec="#333", label="Expanded"),
                       Patch(fc=COLORS["pruned"], ec="#333", label="Pruned (LB ≥ best known)"),
                       Patch(fc=COLORS["optimal"], ec="green", label="Optimal tour")],
              loc="lower left", fontsize=8)
    ax.set_title(title, fontsize=11)
    ax.axis("off")


if __name__ == "__main__":
    nodes, best, best_id, log = solve()
    print("id | path | parent LB + edge + reduction = LB")
    for nd in nodes:
        if nd["parent"] is None:
            print(nd["id"], name(nd["path"]), "| root reduction =", nd["bound"])
        else:
            p = nodes[nd["parent"]]["bound"]
            print(nd["id"], name(nd["path"]), f"| {p} + {nd['edge']} + {nd['red']} = {nd['bound']}")
    print()
    for *_, cap in log:
        print(cap)
    print("\nOptimal cost:", best, "| tour:", name(nodes[best_id]["path"] + [0]))

    pos = layout(nodes)
    final_title = f"TSP (4 cities) – Branch & Bound Search Tree  |  Optimal tour: {name(nodes[best_id]['path'] + [0])}, cost = {best}"
    fig, ax = plt.subplots(figsize=(18, 10))
    vis, st, _ = log[-1]
    draw(ax, nodes, pos, vis, st, final_title)
    plt.tight_layout(); plt.savefig("Visualization.png", dpi=150)

    fig, ax = plt.subplots(figsize=(13, 7.5))
    writer = PillowWriter(fps=1)
    with writer.saving(fig, "demo.gif", dpi=70):
        for vis, st, cap in log:
            draw(ax, nodes, pos, vis, st, "TSP Branch & Bound – " + cap)
            plt.tight_layout()
            writer.grab_frame()
