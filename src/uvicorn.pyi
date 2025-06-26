#!/usr/bin/env python3.13
"""
Type stubs for uvicorn package.
"""

### Standard packages ###
from typing import Any, Callable, Optional, Union

### Local modules ###
from litestar import Litestar

### Type aliases ###
ASGIApplication = Callable[..., Any]
Host = str
Port = int

def run(
  app: Union[str, ASGIApplication, Litestar],
  *,
  host: Host = "127.0.0.1",
  port: Port = 8000,
  uds: Optional[str] = None,
  fd: Optional[int] = None,
  loop: Optional[str] = None,
  http: Optional[str] = None,
  ws: Optional[str] = None,
  ws_ping_interval: Optional[float] = None,
  ws_ping_timeout: Optional[float] = None,
  ws_max_size: int = 16777216,
  lifespan: Optional[str] = None,
  env_file: Optional[str] = None,
  log_config: Optional[Union[dict[str, Any], str]] = None,
  log_level: Optional[Union[str, int]] = None,
  access_log: bool = True,
  use_colors: Optional[bool] = None,
  interface: str = "auto",
  reload: bool = False,
  reload_dirs: Optional[list[str]] = None,
  reload_delay: float = 0.25,
  reload_excludes: Optional[list[str]] = None,
  reload_includes: Optional[list[str]] = None,
  workers: Optional[int] = None,
  proxy_headers: bool = True,
  server_header: bool = True,
  date_header: bool = True,
  forwarded_allow_ips: Optional[Union[str, list[str]]] = None,
  root_path: str = "",
  limit_concurrency: Optional[int] = None,
  limit_max_requests: Optional[int] = None,
  backlog: int = 2048,
  timeout_keep_alive: int = 5,
  ssl_keyfile: Optional[str] = None,
  ssl_certfile: Optional[Union[str, list[str]]] = None,
  ssl_keyfile_password: Optional[str] = None,
  ssl_version: Optional[int] = None,
  ssl_cert_reqs: Optional[int] = None,
  ssl_ca_certs: Optional[str] = None,
  ssl_ciphers: Optional[str] = None,
  headers: Optional[list[tuple[str, str]]] = None,
  **kwargs: Any,
) -> None: ...

### Classes ###
class Config:
  """Configuration class for uvicorn server."""

  def __init__(
    self,
    app: Union[str, ASGIApplication],
    *,
    host: Host = "127.0.0.1",
    port: Port = 8000,
    uds: Optional[str] = None,
    fd: Optional[int] = None,
    loop: Optional[str] = None,
    http: Optional[str] = None,
    ws: Optional[str] = None,
    ws_ping_interval: Optional[float] = None,
    ws_ping_timeout: Optional[float] = None,
    ws_max_size: int = 16777216,
    lifespan: Optional[str] = None,
    env_file: Optional[str] = None,
    log_config: Optional[Union[dict[str, Any], str]] = None,
    log_level: Optional[Union[str, int]] = None,
    access_log: bool = True,
    use_colors: Optional[bool] = None,
    interface: str = "auto",
    reload: bool = False,
    reload_dirs: Optional[list[str]] = None,
    reload_delay: float = 0.25,
    reload_excludes: Optional[list[str]] = None,
    reload_includes: Optional[list[str]] = None,
    workers: Optional[int] = None,
    proxy_headers: bool = True,
    server_header: bool = True,
    date_header: bool = True,
    forwarded_allow_ips: Optional[Union[str, list[str]]] = None,
    root_path: str = "",
    limit_concurrency: Optional[int] = None,
    limit_max_requests: Optional[int] = None,
    backlog: int = 2048,
    timeout_keep_alive: int = 5,
    ssl_keyfile: Optional[str] = None,
    ssl_certfile: Optional[Union[str, list[str]]] = None,
    ssl_keyfile_password: Optional[str] = None,
    ssl_version: Optional[int] = None,
    ssl_cert_reqs: Optional[int] = None,
    ssl_ca_certs: Optional[str] = None,
    ssl_ciphers: Optional[str] = None,
    headers: Optional[list[tuple[str, str]]] = None,
    **kwargs: Any,
  ) -> None: ...
  def load(self) -> None: ...

class Server:
  """Server class for uvicorn."""

  def __init__(self, config: Config) -> None: ...
  def run(self) -> None: ...
  def install_signal_handlers(self) -> None: ...
  def handle_exit(self, sig: int, frame: Any) -> None: ...

### Constants ###
# Common interfaces
INTERFACE_ASGI3: str = "asgi3"
INTERFACE_ASGI2: str = "asgi2"
INTERFACE_WSGI: str = "wsgi"

# Common HTTP protocols
HTTP_PROTOCOLS: dict[str, str] = {
  "auto": "auto",
  "h11": "h11",
  "httptools": "httptools",
}

# Common WebSocket protocols
WS_PROTOCOLS: dict[str, str] = {
  "auto": "auto",
  "none": "none",
  "websockets": "websockets",
  "wsproto": "wsproto",
}

# Common lifespan protocols
LIFESPAN_PROTOCOLS: dict[str, str] = {
  "auto": "auto",
  "on": "on",
  "off": "off",
}

__all__: tuple[str, ...] = (
  "run",
  "Config",
  "Server",
  "ASGIApplication",
  "Host",
  "Port",
  "INTERFACE_ASGI3",
  "INTERFACE_ASGI2",
  "INTERFACE_WSGI",
  "HTTP_PROTOCOLS",
  "WS_PROTOCOLS",
  "LIFESPAN_PROTOCOLS",
)
