import io

from keymanager.onqlave_types.types import AlgorithmDeserialiser

class EncryptedStreamProcessor:
    def __init__(self, cipher_stream: io.BytesIO) -> None:
        self._cipher_stream = cipher_stream

    def read_header(self):
        header_len_buffer = bytearray(4)
        data_len = self._cipher_stream.readinto(header_len_buffer)

        if data_len < 4:
            raise Exception # invalid cipher data
        
        header_len = int.from_bytes(header_len_buffer,byteorder='big')
        header_buffer = bytearray(header_len - 4)
        # should try catch this command
        try:
            data_len = self._cipher_stream.readinto(header_buffer)
        except Exception as exc:
            raise exc
        
        if data_len < header_len - 4:
            raise Exception # invalid cipher data
        
        # should also try catch this command too
        algorithm = AlgorithmDeserialiser()
        algorithm.deserialise(buffer=header_len_buffer + header_buffer)

        return algorithm
    
    def read_packet(self):
        packet_len_buffer = bytearray(4)
        # should try catch this command
        data_len = self._cipher_stream.read(packet_len_buffer)
        
        if data_len < 4:
            raise Exception # invalid cipher data
        
        packet_len = int.from_bytes(packet_len_buffer,'big')
        buffer =bytearray(packet_len)
        data_len = self._cipher_stream.read(buffer)

        if data_len < int(packet_len):
            raise Exception # invalid cipher data
        
        return buffer