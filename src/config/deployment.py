from typing import NamedTuple, Optional

class DeploymentConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to deployment
    
    Attributes:
        host: Host to bind to.
        port: Port to listen for connections.
        domain: Domain name under which this instance is hosted.
        https: Tell Priviblur that is supports HTTPs.

        workers: Amount of worker Priviblur instances to spawn.
            Increases speed significantly

        forwarded_secret:
            https://sanic.dev/en/guide/advanced/proxy-headers.html#forwarded-header
        real_ip_header:
            https://sanic.dev/en/guide/advanced/proxy-headers.html#ip-headers
        proxies_count:
            https://sanic.dev/en/guide/advanced/proxy-headers.html#x-forwarded-for
          
    """

    host: str = "127.0.0.1"
    port: int = 8080
    domain: Optional[str] = None
    https: bool = False

    workers: int = 1

    forwarded_secret: Optional[str] = None
    real_ip_header: Optional[str] = None
    proxies_count: Optional[int] = None
    