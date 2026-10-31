from mazes import get_small_maze
from solver import Solver


def banner(title: str) -> None:
    border = "=" * (len(title) + 8)
    print(border)
    print(f"=== {title} ===")
    print(border)


def main() -> None:
    maze = get_small_maze()
    solver = Solver(maze)

    banner("Original maze")
    for row in maze.render():
        print(row)
    print()

    banner("Solver output")
    path = solver.solve()
    if path is None:
        print("No path found.")
        return

    print(f"Path length: {len(path)}")
    for row in maze.render_with_path(path):
        print(row)


if __name__ == "__main__":
    main()
