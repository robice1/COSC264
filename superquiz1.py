def compose_header(version, hdrlen, tosdscp, totallength, identification, flags, fragmentoffset, timetolive, protocoltype, headerchecksum, sourceaddress, destinationaddress):
    if version != 4:
        raise ValueError("version field must be 4")    
    check_valid("hdrlen", hdrlen, 4)
    check_valid("tosdscp", tosdscp, 6)
    check_valid("totallength", totallength, 16)
    check_valid("identification", identification, 16)
    check_valid("flags", flags, 3)
    check_valid("fragmentoffset", fragmentoffset, 13)
    check_valid("timetolive", timetolive, 8)
    check_valid("protocoltype", protocoltype, 8)
    check_valid("headerchecksum", headerchecksum, 16)
    check_valid("sourceaddress", sourceaddress, 32)
    check_valid("destinationaddress", destinationaddress, 32)
    
    version_hdrlen = (version << 4) | hdrlen
    tosdscp_field = (tosdscp << 2) 
    flags_fragmentoffset = (flags << 13) | fragmentoffset

    
    header = bytearray()
    header.extend(
           [
               version_hdrlen,
               tosdscp_field,
               (totallength >> 8) & 0xFF,
               totallength & 0xFF,
               (identification >> 8) & 0xFF,
               identification & 0xFF,
               (flags_fragmentoffset >> 8) & 0xFF,
               flags_fragmentoffset & 0xFF,
               timetolive,
               protocoltype,
               (headerchecksum >> 8) & 0xFF,
               headerchecksum & 0xFF,
               (sourceaddress >> 24) & 0xFF,
               (sourceaddress >> 16) & 0xFF,
               (sourceaddress >> 8) & 0xFF,
               sourceaddress & 0xFF,
               (destinationaddress >> 24) & 0xFF,
               (destinationaddress >> 16) & 0xFF,
               (destinationaddress >> 8) & 0xFF,
               destinationaddress & 0xFF,
           ]
       )
    return header

def check_valid(name, value, bits):
    max_value = (2**bits) - 1
    if value < 0 or value > max_value:
        raise ValueError(f"{name} value cannot fit in {bits} bits")
   
def basic_packet_check(packet):
    if len(packet) < 20:
        raise ValueError("Packet does not contain a full IP header")
    totallength = (packet[2] << 8) + packet[3]    
    if len(packet) != totallength:
        raise ValueError("Packet totallength field is inconsistent with the packet length")    
    version = packet[0] >> 4    
    if version != 4:
        raise ValueError("Packet version number must equal 4")
    x = 0
    for i in range(10):
        x += (packet[i * 2] << 8) + (packet[i * 2 + 1])
        while x > 0xFFFF:
            x = (x & 0xFFFF) + (x >> 16)
    if x != 0xFFFF:
        raise ValueError("Packet checksum failed")
    return True

def destination_address(packet):
    addr = (packet[16] << 24) + (packet[17] << 16) + (packet[18] << 8) + packet[19]
    dd = f"{addr >> 24}.{(addr >> 16) & 0xFF}.{(addr >> 8) & 0xFF}.{addr & 0xFF}"
    return addr, dd

def payload(packet):
    header_length = (packet[0] & 0x0F) * 4
    payload = packet[header_length:]
    return payload

def compose_packet(hdrlen, tosdscp, identification, flags, fragmentoffset, timetolive, protocoltype, sourceaddress, destinationaddress, payload):
    if hdrlen < 5 or hdrlen > 15:
        raise ValueError("hdrlen must be at least 5 and no greater than 15")
    
    check_valid("tosdscp", tosdscp, 6)
    check_valid("identification", identification, 16)
    check_valid("flags", flags, 3)
    check_valid("fragmentoffset", fragmentoffset, 13)
    check_valid("timetolive", timetolive, 8)
    check_valid("protocoltype", protocoltype, 8)
    check_valid("sourceaddress", sourceaddress, 32)
    check_valid("destinationaddress", destinationaddress, 32)
    
    header_length = hdrlen * 4
    total_length = header_length + len(payload)
    version_hdrlen = (4 << 4) | hdrlen
    tosdscp_field = (tosdscp << 2)
    flags_fragmentoffset = (flags << 13) | fragmentoffset
    header = bytearray()
    header.extend(
        [
            version_hdrlen,
            tosdscp_field,
            (total_length >> 8) & 0xFF,
            total_length & 0xFF,
            (identification >> 8) & 0xFF,
            identification & 0xFF,
            (flags_fragmentoffset >> 8) & 0xFF,
            flags_fragmentoffset & 0xFF,
            timetolive,
            protocoltype,
            0,
            0,
            (sourceaddress >> 24) & 0xFF,
            (sourceaddress >> 16) & 0xFF,
            (sourceaddress >> 8) & 0xFF,
            sourceaddress & 0xFF,
            (destinationaddress >> 24) & 0xFF,
            (destinationaddress >> 16) & 0xFF,
            (destinationaddress >> 8) & 0xFF,
            destinationaddress & 0xFF,
        ]
    )
    
    x = 0
    for i in range(header_length // 2):
        if (i * 2 + 1) < len(header):
            x += (header[i * 2] << 8) + header[i*2 + 1]
        while x > 0xFFFF:
            x = (x & 0xFFFF) + (x >> 16)
    x = ~x & 0xFFFF
    header[10] = (x >> 8) & 0xFF
    header[11] = x & 0xFF
    header.extend(bytearray(header_length - 20))
    packet = header + payload
    return packet

    

packet = compose_packet(6, 24, 4711, 0, 22, 64, 0x06, 0x22334455, 0x66778899, bytearray([0x10, 0x11, 0x12, 0x13, 0x14, 0x15]))
print(packet.hex())