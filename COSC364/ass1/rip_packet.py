import struct
from typing import List, Tuple

class RIPPacket:
    HEADER_FORMAT = "!BBH"  # command(1), version(1), router_id(2)
    ENTRY_FORMAT = "!HHI"   # AFI(2), router_id(2), metric(4)
    
    def __init__(self, command: int, version: int, router_id: int):
        self.command = command
        self.version = version
        self.router_id = router_id
        self.entries: List[Tuple[int, int]] = []  # List of (destination, metric)

    def add_entry(self, destination: int, metric: int):
        self.entries.append((destination, metric))

    def to_bytes(self) -> bytes:
        """Convert RIP packet to bytes for transmission"""
        header = struct.pack(self.HEADER_FORMAT, self.command, self.version, self.router_id)
        
        entries = bytearray()
        for dest, metric in self.entries:
            entries.extend(struct.pack(self.ENTRY_FORMAT, 2, dest, metric))
            
        return header + entries

    @classmethod
    def from_bytes(cls, data: bytes) -> 'RIPPacket':
        """Create RIP packet from received bytes"""
        if len(data) < 4:
            raise ValueError("Packet too short")
            
        command, version, router_id = struct.unpack(cls.HEADER_FORMAT, data[:4])
        packet = cls(command, version, router_id)
        
        # Parse entries
        pos = 4
        while pos + 8 <= len(data):
            afi, dest, metric = struct.unpack(cls.ENTRY_FORMAT, data[pos:pos + 8])
            if afi != 2:  # AFI must be 2 for IP
                raise ValueError("Invalid AFI")
            packet.add_entry(dest, metric)
            pos += 8
            
        return packet
