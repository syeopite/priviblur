from typing import NamedTuple, Optional

class DeploymentConfig(NamedTuple):
    """NamedTuple that stores configuration values relating to deployment
    
    Attributes:
        host: Host to bind to.
        port: Port to listen for connections.
        domain: Domain name under which this instance is hosted.

        https: Enables secure cookies and forces all links to priviblur to use the `https://` scheme

        workers: Amount of worker Priviblur instances to spawn.
            Increases speed significantly          
    """

    host: str = "127.0.0.1"
    port: int = 8080
    domain: Optional[str] = None

    https: bool = False

    workers: int = 1
