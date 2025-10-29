"""
Envoy xDS Control Plane
Manages configuration for multiple Envoy proxy instances using xDS protocol
"""

import grpc
from concurrent import futures
import time
import logging
from typing import Dict, List

# Envoy xDS API imports
from envoy.service.discovery.v3 import discovery_pb2, discovery_pb2_grpc
from envoy.config.listener.v3 import listener_pb2
from envoy.config.route.v3 import route_pb2
from envoy.config.cluster.v3 import cluster_pb2
from envoy.config.endpoint.v3 import endpoint_pb2
from google.protobuf import any_pb2
from google.protobuf.duration_pb2 import Duration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnvoyControlPlane(discovery_pb2_grpc.AggregatedDiscoveryServiceServicer):
    """
    xDS Control Plane for Envoy Proxies
    Implements ADS (Aggregated Discovery Service)
    """

    def __init__(self):
        self.version = "1"
        self.connected_proxies: Dict[str, dict] = {}
        logger.info("Control Plane initialized")

    def StreamAggregatedResources(self, request_iterator, context):
        """
        Handle bidirectional streaming for xDS protocol
        """
        node_id = None

        try:
            for request in request_iterator:
                if not node_id and request.node.id:
                    node_id = request.node.id
                    self.connected_proxies[node_id] = {
                        "cluster": request.node.cluster,
                        "connected_at": time.time()
                    }
                    logger.info(f"Proxy connected: {node_id} (cluster: {request.node.cluster})")

                # Handle different resource types
                type_url = request.type_url
                logger.info(f"Received {type_url} request from {node_id}")

                if "Listener" in type_url:
                    response = self._build_listener_response(request)
                elif "RouteConfiguration" in type_url:
                    response = self._build_route_response(request)
                elif "Cluster" in type_url:
                    response = self._build_cluster_response(request)
                elif "ClusterLoadAssignment" in type_url:
                    response = self._build_endpoint_response(request)
                else:
                    logger.warning(f"Unknown resource type: {type_url}")
                    continue

                yield response

        except grpc.RpcError as e:
            logger.error(f"gRPC error for {node_id}: {e}")
        finally:
            if node_id and node_id in self.connected_proxies:
                del self.connected_proxies[node_id]
                logger.info(f"Proxy disconnected: {node_id}")

    def _build_listener_response(self, request):
        """Build Listener Discovery Service (LDS) response"""
        logger.info("Building listener configuration")

        # Create HTTP listener
        listener = listener_pb2.Listener(
            name="http_listener",
            # Additional listener configuration would go here
        )

        response = discovery_pb2.DiscoveryResponse(
            version_info=self.version,
            type_url=request.type_url,
            nonce=str(time.time())
        )

        # Pack listener into Any
        resource = any_pb2.Any()
        resource.Pack(listener)
        response.resources.append(resource)

        return response

    def _build_route_response(self, request):
        """Build Route Discovery Service (RDS) response"""
        logger.info("Building route configuration")

        response = discovery_pb2.DiscoveryResponse(
            version_info=self.version,
            type_url=request.type_url,
            nonce=str(time.time())
        )

        return response

    def _build_cluster_response(self, request):
        """Build Cluster Discovery Service (CDS) response"""
        logger.info("Building cluster configuration")

        clusters = []

        # GraphQL Cluster
        graphql_cluster = cluster_pb2.Cluster(
            name="graphql_service",
            connect_timeout=Duration(seconds=5),
            type=cluster_pb2.Cluster.STRICT_DNS,
            lb_policy=cluster_pb2.Cluster.ROUND_ROBIN
        )
        clusters.append(graphql_cluster)

        # REST Cluster
        rest_cluster = cluster_pb2.Cluster(
            name="rest_service",
            connect_timeout=Duration(seconds=5),
            type=cluster_pb2.Cluster.STRICT_DNS,
            lb_policy=cluster_pb2.Cluster.ROUND_ROBIN
        )
        clusters.append(rest_cluster)

        # gRPC Cluster
        grpc_cluster = cluster_pb2.Cluster(
            name="grpc_service",
            connect_timeout=Duration(seconds=5),
            type=cluster_pb2.Cluster.STRICT_DNS,
            lb_policy=cluster_pb2.Cluster.ROUND_ROBIN
        )
        clusters.append(grpc_cluster)

        response = discovery_pb2.DiscoveryResponse(
            version_info=self.version,
            type_url=request.type_url,
            nonce=str(time.time())
        )

        for cluster in clusters:
            resource = any_pb2.Any()
            resource.Pack(cluster)
            response.resources.append(resource)

        logger.info(f"Sent {len(clusters)} clusters")
        return response

    def _build_endpoint_response(self, request):
        """Build Endpoint Discovery Service (EDS) response"""
        logger.info("Building endpoint configuration")

        response = discovery_pb2.DiscoveryResponse(
            version_info=self.version,
            type_url=request.type_url,
            nonce=str(time.time())
        )

        return response

    def get_connected_proxies(self) -> Dict[str, dict]:
        """Get list of connected proxies"""
        return self.connected_proxies.copy()

    def update_configuration(self, config_type: str, config_data: dict):
        """
        Update configuration and push to all connected proxies
        This would be called by a management API
        """
        self.version = str(int(self.version) + 1)
        logger.info(f"Configuration updated: type={config_type}, version={self.version}")
        # In a real implementation, this would trigger pushes to all proxies


def serve():
    """Start the xDS control plane server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    control_plane = EnvoyControlPlane()

    discovery_pb2_grpc.add_AggregatedDiscoveryServiceServicer_to_server(
        control_plane, server
    )

    port = "18000"
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    logger.info(f"xDS Control Plane started on port {port}")
    logger.info("Waiting for Envoy proxies to connect...")

    try:
        while True:
            time.sleep(60)
            connected = control_plane.get_connected_proxies()
            logger.info(f"Connected proxies: {len(connected)}")
            for proxy_id, info in connected.items():
                logger.info(f"  - {proxy_id}: {info}")
    except KeyboardInterrupt:
        logger.info("Shutting down control plane...")
        server.stop(0)


if __name__ == "__main__":
    serve()
