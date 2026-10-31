from maze import Maze


def get_render_maze() -> Maze:
    return Maze(
        [
            "#####",
            "#S..#",
            "#.#.#",
            "#..E#",
            "#####",
        ]
    )


def get_small_maze() -> Maze:
    return Maze(
        [
            "#######",
            "#S....#",
            "#.###.#",
            "#.#...#",
            "#.#.#.#",
            "#...#E#",
            "#######",
        ]
    )


def get_blocked_maze() -> Maze:
    return Maze(
        [
            "#####",
            "#S#E#",
            "#####",
        ]
    )


def get_anywhere_start_end_maze() -> Maze:
    return Maze(
        [
            "#######",
            "#..E..#",
            "#.###.#",
            "#S....#",
            "#######",
        ]
    )


def get_directional_passage_maze() -> Maze:
    return Maze(
        [
            "#######",
            "#S.>E##",
            "#######",
        ]
    )


def get_directional_blocked_entry_maze() -> Maze:
    return Maze(
        [
            "#######",
            "#S<.E##",
            "#######",
        ]
    )


def get_directional_blocked_exit_maze() -> Maze:
    return Maze(
        [
            "#######",
            "#S.>###",
            "###.E##",
            "#######",
        ]
    )


def get_door_without_key_maze() -> Maze:
    return Maze(
        [
            "#######",
            "#S.AE##",
            "#######",
        ]
    )


def get_key_door_maze() -> Maze:
    return Maze(
        [
            "########",
            "#S.aAE##",
            "########",
        ]
    )


def get_key_backtrack_maze() -> Maze:
    return Maze(
        [
            "########",
            "#S.A..E#",
            "#.#.##.#",
            "#a#....#",
            "########",
        ]
    )
