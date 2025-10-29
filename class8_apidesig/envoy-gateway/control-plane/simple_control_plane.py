"""
Simple Control Plane for Envoy Proxies
Manages configuration via REST API and file-based updates
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import yaml
import os
import logging
from datetime import datetime
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Envoy Control Plane", version="1.0.0")


class ServiceEndpoint(BaseModel):
    """Service endpoint configuration"""
    name: str
    address: str
    port: int
    protocol: str  # http, grpc, https
    health_check_path: Optional[str] = "/health"


class RouteConfig(BaseModel):
    """Route configuration"""
    path: str
    service: str
    timeout_seconds: int = 30
    retry_policy: Optional[dict] = None


class EnvoyProxyStatus(BaseModel):
    """Status of an Envoy proxy instance"""
    id: str
    status: str  # active, inactive, unhealthy
    last_updated: str
    version: str
    endpoints: Dict[str, str]


class ControlPlane:
    """Control plane state manager"""

    def __init__(self, config_dir: str = "/tmp/envoy-config"):
        self.config_dir = config_dir
        self.services: Dict[str, ServiceEndpoint] = {}
        self.routes: List[RouteConfig] = []
        self.proxies: Dict[str, EnvoyProxyStatus] = {}
        self.config_version = 1

        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)

        # Initialize with default services
        self._initialize_default_services()
        logger.info("Control Plane initialized")

    def _initialize_default_services(self):
        """Initialize with default backend services"""
        default_services = [
            ServiceEndpoint(
                name="rest-api",
                address="rest-api",
                port=8000,
                protocol="http",
                health_check_path="/health"
            ),
            ServiceEndpoint(
                name="grpc-api",
                address="grpc-api",
                port=50051,
                protocol="grpc",
                health_check_path=""
            ),
            ServiceEndpoint(
                name="graphql-api",
                address="graphql-api",
                port=8000,
                protocol="http",
                health_check_path="/health"
            )
        ]

        for service in default_services:
            self.services[service.name] = service

        # Default routes
        self.routes = [
            RouteConfig(path="/graphql", service="graphql-api", timeout_seconds=30),
            RouteConfig(path="/api/", service="rest-api", timeout_seconds=15),
            RouteConfig(path="/grpc/", service="grpc-api", timeout_seconds=30)
        ]

    def register_proxy(self, proxy_id: str, endpoints: Dict[str, str]):
        """Register a new Envoy proxy instance"""
        self.proxies[proxy_id] = EnvoyProxyStatus(
            id=proxy_id,
            status="active",
            last_updated=datetime.now().isoformat(),
            version=str(self.config_version),
            endpoints=endpoints
        )
        logger.info(f"Proxy registered: {proxy_id}")

    def update_proxy_status(self, proxy_id: str, status: str):
        """Update proxy status"""
        if proxy_id in self.proxies:
            self.proxies[proxy_id].status = status
            self.proxies[proxy_id].last_updated = datetime.now().isoformat()
            logger.info(f"Proxy {proxy_id} status updated: {status}")

    def add_service(self, service: ServiceEndpoint):
        """Add a new service"""
        self.services[service.name] = service
        self.config_version += 1
        self._regenerate_envoy_config()
        logger.info(f"Service added: {service.name}")

    def remove_service(self, service_name: str):
        """Remove a service"""
        if service_name in self.services:
            del self.services[service_name]
            self.config_version += 1
            self._regenerate_envoy_config()
            logger.info(f"Service removed: {service_name}")

    def add_route(self, route: RouteConfig):
        """Add a new route"""
        self.routes.append(route)
        self.config_version += 1
        self._regenerate_envoy_config()
        logger.info(f"Route added: {route.path} -> {route.service}")

    def _regenerate_envoy_config(self):
        """Regenerate Envoy configuration files"""
        config = self._build_envoy_config()

        # Write configuration for each proxy
        for proxy_id in self.proxies.keys():
            config_file = os.path.join(self.config_dir, f"envoy-{proxy_id}.yaml")
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)

            logger.info(f"Configuration updated for proxy {proxy_id}")

    def _build_envoy_config(self) -> dict:
        """Build Envoy configuration dictionary"""
        clusters = []

        for service_name, service in self.services.items():
            cluster = {
                "name": service_name,
                "connect_timeout": "5s",
                "type": "STRICT_DNS",
                "lb_policy": "ROUND_ROBIN",
                "load_assignment": {
                    "cluster_name": service_name,
                    "endpoints": [{
                        "lb_endpoints": [{
                            "endpoint": {
                                "address": {
                                    "socket_address": {
                                        "address": service.address,
                                        "port_value": service.port
                                    }
                                }
                            }
                        }]
                    }]
                }
            }

            if service.protocol == "grpc":
                cluster["http2_protocol_options"] = {}

            if service.health_check_path:
                cluster["health_checks"] = [{
                    "timeout": "5s",
                    "interval": "10s",
                    "unhealthy_threshold": 3,
                    "healthy_threshold": 2,
                    "http_health_check": {
                        "path": service.health_check_path
                    }
                }]

            clusters.append(cluster)

        # Build routes
        routes_config = []
        for route in self.routes:
            routes_config.append({
                "match": {"prefix": route.path},
                "route": {
                    "cluster": route.service,
                    "timeout": f"{route.timeout_seconds}s"
                }
            })

        config = {
            "static_resources": {
                "clusters": clusters
            },
            "version": str(self.config_version)
        }

        return config

    def get_status(self) -> dict:
        """Get control plane status"""
        return {
            "version": self.config_version,
            "services": len(self.services),
            "routes": len(self.routes),
            "proxies": len(self.proxies),
            "timestamp": datetime.now().isoformat()
        }


# Global control plane instance
control_plane = ControlPlane()


# REST API Endpoints

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "Envoy Control Plane",
        "version": "1.0.0",
        "endpoints": {
            "/status": "Get control plane status",
            "/services": "List all services",
            "/services/add": "Add a new service",
            "/routes": "List all routes",
            "/proxies": "List registered proxies"
        }
    }


@app.get("/status")
def get_status():
    """Get control plane status"""
    return control_plane.get_status()


@app.get("/services")
def list_services():
    """List all registered services"""
    return {"services": list(control_plane.services.values())}


@app.post("/services/add")
def add_service(service: ServiceEndpoint):
    """Add a new service"""
    control_plane.add_service(service)
    return {"message": f"Service {service.name} added", "version": control_plane.config_version}


@app.delete("/services/{service_name}")
def remove_service(service_name: str):
    """Remove a service"""
    if service_name not in control_plane.services:
        raise HTTPException(status_code=404, detail="Service not found")

    control_plane.remove_service(service_name)
    return {"message": f"Service {service_name} removed", "version": control_plane.config_version}


@app.get("/routes")
def list_routes():
    """List all routes"""
    return {"routes": control_plane.routes}


@app.post("/routes/add")
def add_route(route: RouteConfig):
    """Add a new route"""
    control_plane.add_route(route)
    return {"message": "Route added", "version": control_plane.config_version}


@app.get("/proxies")
def list_proxies():
    """List all registered proxies"""
    return {"proxies": list(control_plane.proxies.values())}


@app.post("/proxies/register")
def register_proxy(proxy_id: str, endpoints: Dict[str, str]):
    """Register a new proxy"""
    control_plane.register_proxy(proxy_id, endpoints)
    return {"message": f"Proxy {proxy_id} registered"}


@app.post("/proxies/{proxy_id}/status")
def update_proxy_status(proxy_id: str, status: str):
    """Update proxy status"""
    if proxy_id not in control_plane.proxies:
        raise HTTPException(status_code=404, detail="Proxy not found")

    control_plane.update_proxy_status(proxy_id, status)
    return {"message": f"Proxy {proxy_id} status updated"}


@app.get("/config/version")
def get_config_version():
    """Get current configuration version"""
    return {"version": control_plane.config_version}


@app.post("/config/reload")
def reload_configuration():
    """Trigger configuration reload for all proxies"""
    control_plane._regenerate_envoy_config()
    return {
        "message": "Configuration reloaded",
        "version": control_plane.config_version,
        "proxies_updated": len(control_plane.proxies)
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Control Plane on port 8080...")
    uvicorn.run(app, host="0.0.0.0", port=8080)
