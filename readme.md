# Block Breaker

A brick-breaker game built with [pygame-ce](https://pyga.me/), inspired by the Google Doodle "Block Breaker" game. Break bricks, chase rare power-ups, and go head-to-head with a friend in networked Versus mode. Make sure to star this repo!

## Tech stack

- **Python 3** — core language
- **[pygame-ce](https://pyga.me/)** — rendering, input, audio, and the game loop (a community-maintained, actively developed fork of pygame)
- **`socket`** (Python standard library) — TCP networking for Versus mode, using a plain client/server model (host listens, client connects)
- **`threading`** (Python standard library) — runs connection/accept and network receive loops in the background so the game loop never blocks waiting on the network
- **`json`** (Python standard library) — serializes each player's game state into newline-delimited messages sent over the socket

No external services, databases, or build tools — it's a single Python process per player, run directly with the interpreter. High scores are persisted locally as a JSON file, no server required.

## Requirements

- Python 3.9+
- [pygame-ce](https://pyga.me/)

Install the dependency with:

```bash
pip install pygame-ce
```

## Running the game

From the project root:

```bash
python main.py
```

This launches in fullscreen. From the main menu, choose **Solo** for single-player, or **Versus** for networked multiplayer.

### Windowed mode (for local testing)

To run in a small window instead of fullscreen — handy for testing two instances on one machine — pass the `--windowed` flag:

```bash
python main.py --windowed
```

## Playing Versus mode

Versus mode connects two players over the same local network (LAN) — same wifi/router. It does **not** work across separate networks or over the internet.

1. Both players select **Versus** from the main menu and pick the **same difficulty**.
2. One player selects **Host Game**. Their screen will display their local IP address and wait for a connection.
3. The other player selects **Join Game**, types in the host's IP address, and connects.
4. Once connected, both players are dropped straight into a live split-screen match — your board on the left, your opponent's on the right.
5. Press **Space** or click to launch your ball. **Esc** disconnects and returns to the menu.

**Troubleshooting a failed connection:**
- Make sure the Host reaches the "Waiting for opponent..." screen *before* the Joiner tries to connect.
- Double-check both devices are on the same network (some guest wifi networks block device-to-device traffic).
- The Host's machine may show a firewall prompt the first time it starts listening — it needs to be allowed through for the connection to succeed.

## Controls

| Action | Key |
|---|---|
| Move paddle | Arrow keys or A / D |
| Launch ball | Space or left-click |
| Back / quit to menu | Esc |

## Known limitations / roadmap

- Versus mode's end-of-match screen currently reports only your own result, not an explicit win/loss based on both players.
- If the connection drops mid-match, the game currently just ends the match rather than offering to reconnect.
- Versus mode is LAN-only; there's no support yet for play across separate networks/the internet.
- Controller support is planned but not yet implemented (keyboard only for now).