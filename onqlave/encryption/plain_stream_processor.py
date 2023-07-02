import io
import struct

from keymanager.onqlave_types.types import AlgorithmSerialiser
class PlainStreamProcessor:
    def __init__(self,cipher_stream: io.BytesIO) -> None:
        self._cipher_stream = cipher_stream

    def write_header(self, algorithm: AlgorithmSerialiser):
        header = algorithm.serialise()
        try:
            self._cipher_stream.write(header)
        except Exception as exc:
            raise exc # need to handle this specifically
        
    
    def write_packet(self, packet: bytearray):
        data_len = struct.pack(">I",len(packet))
        try:
            self._cipher_stream.write(data_len)
             # confirm with Matt to make sure what this means
            self._cipher_stream.write(packet)
        except Exception as exc:
            raise exc