"""
Reliable Transport Starter Code

This module contains the starter code for implementing reliable transport protocols.
Students should implement the methods as instructed in the docstrings.
You are supposed to implement the SELECTIVE REPEAT protocol of sliding window.
"""

import socket
import queue
import util  # Assuming util provides make_packet, parse_packet, and validate_checksum
from typing import Tuple
from dataclasses import dataclass
import time
import random
import collections

Address = Tuple[str, int]

@dataclass
class MessageSender:
    '''
    DO NOT EDIT ANYTHING IN THIS CLASS

    Base class for sending messages over a socket.
    Handles the mechanics of sending a formatted packet to the receiver.
    '''
    sock: socket
    receiver_addr: Address
    msg_id: int

    def send(self, packet: str):
        """
        Send a packet to the receiver.

        Args:
            packet (str): The packet to send.
        """
        self.sock.sendto(
            f"s:{str(self.msg_id)}:{packet}".encode("utf-8"),
            self.receiver_addr
        )

@dataclass
class ReliableMessageSender(MessageSender):
    '''
    This class reliably delivers a message to a receiver.
    
    You have to implement the send_message and on_packet_received methods.
    
    You can use self.send(packet) to send a packet to the receiver.
    
    You can add as many helper functions as you want.
    '''
    window_size: int
    unacked_packets: dict = None
    
    def __post_init__(self):
        self.unacked_packets = {}
        self.base_seq = None
    
    def send_message(self, message: str):
        """
        Implements reliable message sending using the Selective Repeat protocol.
        """
        chunks = [message[i:i + util.CHUNK_SIZE] for i in range(0, len(message), util.CHUNK_SIZE)]
        total_chunks = len(chunks)
        self.base_seq = random.randint(1000, 9999)
        
        self.send(util.make_packet("start", self.base_seq, ""))
        self.wait_for_ack(self.base_seq)
        
        next_seq = self.base_seq + 1
        while next_seq < self.base_seq + total_chunks + 1:
            for i in range(self.window_size):
                seq = self.base_seq + i
                if seq < self.base_seq + total_chunks and seq not in self.unacked_packets:
                    packet = util.make_packet("data", seq, chunks[seq - self.base_seq])
                    self.send(packet)
                    self.unacked_packets[seq] = packet
            
            self.handle_timeouts()
            next_seq += 1
        
        self.send(util.make_packet("end", next_seq, ""))
        self.wait_for_ack(next_seq)

    def wait_for_ack(self, seq):
        while seq in self.unacked_packets:
            try:
                ack_packet, _ = self.sock.recvfrom(util.BUFFER_SIZE)
                pkt_type, ack_seq, _, _ = util.parse_packet(ack_packet.decode())
                ack_seq = int(ack_seq)
                if pkt_type == "ack" and ack_seq in self.unacked_packets:
                    del self.unacked_packets[ack_seq]
            except socket.timeout:
                self.handle_timeouts()
    
    def handle_timeouts(self):
        """
        Retransmit only the lost packets instead of all packets in the window.
        """
        for seq in list(self.unacked_packets.keys()):
            self.send(self.unacked_packets[seq])
    
    def on_packet_received(self, packet):
        pkt_type, seq_num, _, _ = util.parse_packet(packet)
        seq_num = int(seq_num)
        if pkt_type == "ack" and seq_num in self.unacked_packets:
            del self.unacked_packets[seq_num]

@dataclass
class MessageReceiver:
    '''
    DO NOT EDIT ANYTHING IN THIS CLASS
    '''
    sock: socket
    sender_addr: Address
    msg_id: int
    completed_message_q: queue.Queue

    def send(self, packet: str):
        """
        Send a packet back to the sender.

        Args:
            packet (str): The packet to send.
        """
        self.sock.sendto(
            f"r:{str(self.msg_id)}:{packet}".encode("utf-8"),
            self.sender_addr
        )

    def on_message_completed(self, message: str):
        """
        Notify that a complete message has been received.

        Args:
            message (str): The complete message received.
        """
        self.completed_message_q.put(message)

@dataclass
class ReliableMessageReceiver(MessageReceiver):
    '''
    This class reliably receives a message from a sender. 
    You have to implement the on_packet_received method. 
    '''
    received_packets: dict = None  
    expected_seq: int = None  
    
    def __post_init__(self):
        self.received_packets = {}
        self.expected_seq = None
    
    def on_packet_received(self, packet: str):
        """
        Handles incoming packets and acknowledges received data.
        """
        pkt_type, seq_num, data, checksum = util.parse_packet(packet)
        seq_num = int(seq_num)
        
        if not util.validate_checksum(packet):
            return
        
        if pkt_type == "start":
            self.expected_seq = seq_num + 1
            self.send(util.make_packet("ack", self.expected_seq, ""))
        
        elif pkt_type == "data":
            if seq_num not in self.received_packets:
                self.received_packets[seq_num] = data
            
            ack_num = min([seq for seq in range(self.expected_seq, seq_num + 1) if seq in self.received_packets], default=self.expected_seq)
            self.send(util.make_packet("ack", ack_num, ""))
            if ack_num == self.expected_seq:
                self.expected_seq += 1
        
        elif pkt_type == "end":
            message = "".join(self.received_packets[seq] for seq in sorted(self.received_packets))
            self.send(util.make_packet("ack", seq_num + 1, ""))
            self.on_message_completed(message)
