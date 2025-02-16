import select
import time
from typing import List, Tuple
import socket
from message_handler import MessageHandler
from config_parser import RouterConfig
from rip_types import RoutingTable, INFINITY, UPDATE_INTERVAL
from rip_packet import RIPPacket

class Router:
    def __init__(self, config: RouterConfig):
        self.router_id = config.router_id
        self.input_ports = config.input_ports
        self.neighbor_info = config.neighbor_info
        self.sockets = MessageHandler.setup_sockets(self.input_ports)
        self.routing_table = RoutingTable(self.router_id)
        self.last_update = time.time()
        
        # Initialize routing table with direct neighbors
        for port, cost, neighbor_id in self.neighbor_info:
            self.routing_table.add_route(neighbor_id, neighbor_id, cost)

    def run(self):
        try:
            print(f"Router {self.router_id} initialized")
            self.send_updates()  # Initial update
            
            while True:
                readable, _, _ = select.select(self.sockets, [], [], 1.0)
                current_time = time.time()
                
                # Process incoming messages
                for sock in readable:
                    data, addr = MessageHandler.receive_message(sock)
                    if data:
                        self.process_rip_message(data)
                
                # Send periodic updates
                if current_time - self.last_update >= UPDATE_INTERVAL:
                    self.send_updates()
                    self.last_update = current_time
                
                # Check for route timeouts
                self.routing_table.check_timeouts()
                
        except KeyboardInterrupt:
            print("\nRouter shutting down...")
        finally:
            self._cleanup()

    def process_rip_message(self, data: bytes):
        try:
            packet = RIPPacket.from_bytes(data)
            updated = False
            
            # Process each route in the update
            for destination, metric in packet.entries:
                if destination == self.router_id:
                    continue  # Skip routes to ourselves
                    
                new_metric = min(metric + 1, INFINITY)
                if self.routing_table.update_route(destination, packet.router_id, new_metric):
                    updated = True
                    
            if updated:
                self.send_triggered_update()
                
        except Exception as e:
            print(f"Error processing RIP message: {e}")

    def send_updates(self, triggered=False):
        """Send RIP updates to all neighbors"""
        packet = RIPPacket(command=2, version=2, router_id=self.router_id)
        
        # Add all routes to packet
        for route in self.routing_table.get_routes():
            packet.add_entry(route.destination, route.metric)
        
        # Send to all neighbors
        data = packet.to_bytes()
        for port, _, _ in self.neighbor_info:
            try:
                self.sockets[0].sendto(data, (MessageHandler.LOCALHOST, port))
            except Exception as e:
                print(f"Error sending update to port {port}: {e}")

    def send_triggered_update(self):
        """Send immediate update when routes change"""
        self.send_updates(triggered=True)

    def _cleanup(self):
        for sock in self.sockets:
            sock.close()
