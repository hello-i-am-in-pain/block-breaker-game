import json
import socket
import threading

DEFAULT_PORT = 5555


def get_local_ip():
    """Best-effort guess at this machine's LAN IP, to show the host so
    they can hand it to the other player."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually send any packets - just asks the OS which local
        # interface/IP it would use to reach that address.
        probe.connect(("8.8.8.8", 80))
        return probe.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        probe.close()


class NetworkPeer:
    """Shared plumbing for both ends of a two-player LAN connection.

    Once connected, a Host and a Client behave identically: both can
    send_state() and get_latest_remote_state(). Only how the connection
    gets established differs, which is why that part lives in the
    subclasses below instead of here.
    """

    def __init__(self):
        self._socket = None
        self._reader = None
        self.connected = False
        self.error = None
        self._latest_remote_state = None
        self._lock = threading.Lock()

    def send_state(self, state):
        """Send this machine's local game state to the other player.
        Safe to call every frame - failures just mark the connection
        dead rather than raising into the game loop."""
        if not self.connected or self._socket is None:
            return
        try:
            payload = (json.dumps(state) + "\n").encode("utf-8")
            self._socket.sendall(payload)
        except OSError as exc:
            self._handle_disconnect(exc)

    def get_latest_remote_state(self):
        """The most recent state received from the other player, or None
        if nothing has arrived yet. Never blocks."""
        with self._lock:
            return self._latest_remote_state

    def close(self):
        self.connected = False
        if self._socket is not None:
            try:
                self._socket.close()
            except OSError:
                pass

    def _start_receive_loop(self):
        self._reader = self._socket.makefile("r", encoding="utf-8")
        thread = threading.Thread(target=self._receive_loop, daemon=True)
        thread.start()

    def _receive_loop(self):
        # Each message is one line of JSON. This runs on its own thread
        # for the life of the connection so the main game loop never
        # blocks waiting on the network.
        try:
            for line in self._reader:
                line = line.strip()
                if not line:
                    continue
                try:
                    state = json.loads(line)
                except json.JSONDecodeError:
                    continue
                with self._lock:
                    self._latest_remote_state = state
            self._handle_disconnect(None)
        except OSError as exc:
            self._handle_disconnect(exc)

    def _handle_disconnect(self, exc):
        self.connected = False
        if exc is not None:
            self.error = str(exc)


class Host(NetworkPeer):
    """Opens a listening socket and waits for the other player to join."""

    def __init__(self, port=DEFAULT_PORT):
        super().__init__()
        self.port = port
        self._listen_socket = None
        self.local_ip = get_local_ip()

    def start_hosting(self):
        """Begin listening in the background. Non-blocking - poll
        `connected` (and `error`) from the main loop to find out when a
        client has joined (or the attempt failed)."""
        thread = threading.Thread(target=self._accept_loop, daemon=True)
        thread.start()

    def _accept_loop(self):
        try:
            self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._listen_socket.bind(("", self.port))
            self._listen_socket.listen(1)
            conn, _addr = self._listen_socket.accept()
            self._socket = conn
            self.connected = True
            self._start_receive_loop()
        except OSError as exc:
            self.error = str(exc)


class Client(NetworkPeer):
    """Connects out to a Host at a known LAN IP address."""

    def connect(self, host_ip, port=DEFAULT_PORT):
        """Begin connecting in the background. Non-blocking - poll
        `connected` (and `error`) from the main loop."""
        thread = threading.Thread(
            target=self._connect_loop, args=(host_ip, port), daemon=True
        )
        thread.start()

    def _connect_loop(self, host_ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((host_ip, port))
            sock.settimeout(None)
            self._socket = sock
            self.connected = True
            self._start_receive_loop()
        except OSError as exc:
            self.error = str(exc)