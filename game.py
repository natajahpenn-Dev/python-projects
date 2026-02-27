import os
import random
import time
import sys

WINDOWS = os.name == "nt"
if WINDOWS:
    import msvcrt
else:
    import termios
    import tty
    import select

WIDTH = 25
HEIGHT = 12
TICK = 0.12

player_x = WIDTH // 2
score = 0

blocks = []   # (x, y)
packs = []    # (x, y) health packs

lives = 3
MAX_LIVES = 3

INVINCIBLE_SECONDS = 1.0
invincible_until = 0.0

BLOCK_SPAWN_CHANCE = 0.35
PACK_SPAWN_CHANCE = 0.06  # lower = rarer

def clear():
    os.system("cls" if WINDOWS else "clear")

def get_key():
    if WINDOWS:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            try:
                return key.decode("utf-8").lower()
            except:
                return None
        return None
    else:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1).lower()
        return None

def hearts(n):
    return "❤️" * n + " " * (MAX_LIVES - n)

def draw():
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # blocks
    for x, y in blocks:
        if 0 <= y < HEIGHT:
            grid[y][x] = "#"

    # health packs
    for x, y in packs:
        if 0 <= y < HEIGHT:
            grid[y][x] = "+"

    # player
    grid[HEIGHT - 1][player_x] = "A"

    clear()
    print("DODGE THE BLOCKS  |  A/D move  |  Q quit")
    print(f"Score: {score}   Lives: {hearts(lives)}   (Catch '+' to heal)")
    print("+" + "-" * WIDTH + "+")
    for row in grid:
        print("|" + "".join(row) + "|")
    print("+" + "-" * WIDTH + "+")

def game_over():
    clear()
    print("💥 GAME OVER 💥")
    print(f"Final Score: {score}")
    sys.exit()

def enable_raw_mode():
    if WINDOWS:
        return None
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    return old

def restore_mode(old):
    if (not WINDOWS) and old is not None:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)

def main():
    global player_x, score, blocks, packs, lives, invincible_until

    old_mode = enable_raw_mode()
    try:
        while True:
            now = time.time()

            # spawn block
            if random.random() < BLOCK_SPAWN_CHANCE:
                blocks.append((random.randint(0, WIDTH - 1), 0))

            # spawn health pack (rarer)
            if random.random() < PACK_SPAWN_CHANCE:
                packs.append((random.randint(0, WIDTH - 1), 0))

            # move stuff down
            blocks = [(x, y + 1) for (x, y) in blocks]
            packs = [(x, y + 1) for (x, y) in packs]

            # input
            key = get_key()
            if key == "a":
                player_x = max(0, player_x - 1)
            elif key == "d":
                player_x = min(WIDTH - 1, player_x + 1)
            elif key == "q":
                break

            # --- collision: blocks ---
            hit_block = any((y == HEIGHT - 1 and x == player_x) for x, y in blocks)
            if hit_block and now >= invincible_until:
                lives -= 1
                invincible_until = now + INVINCIBLE_SECONDS

                # remove blocks on player row so you don't instantly re-hit
                blocks = [(x, y) for (x, y) in blocks if y != HEIGHT - 1]

                if lives <= 0:
                    game_over()

            # --- collision: health pack ---
            got_pack = any((y == HEIGHT - 1 and x == player_x) for x, y in packs)
            if got_pack:
                if lives < MAX_LIVES:
                    lives += 1
                # remove packs on player row after pickup
                packs = [(x, y) for (x, y) in packs if y != HEIGHT - 1]

            # score over time
            score += 1

            # remove off screen
            blocks = [(x, y) for x, y in blocks if y < HEIGHT]
            packs = [(x, y) for x, y in packs if y < HEIGHT]

            draw()
            time.sleep(TICK)

    finally:
        restore_mode(old_mode)
        clear()
        print("Bye!")

if __name__ == "__main__":
    main()