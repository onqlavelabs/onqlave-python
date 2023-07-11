import io
import struct

from keymanager.onqlave_types.types import AlgorithmSerialiser
class PlainStreamProcessor:
    """A stream processor for the plain stream in the encryption process
    with two function including writing the header and writing the packet.
    """
    def __init__(self,cipher_stream: io.BytesIO) -> None:
        """Init an PlainStreamProcessor object which takes the cipher stream
        in the encryption process as its main attribute

        Args:
            cipher_stream: a standard python stream object

        Returns:
            Nothing
        """
        self._cipher_stream = cipher_stream

    def write_header(self, algorithm: AlgorithmSerialiser):
        """Serialise the algorithm information to the header

        Args:
            algorithm: an AlgorithmSerialiser object contains information
            about the selected encryption algorithm

        Returns:
            Nothing
        """
        header = algorithm.serialise()
        try:
            self._cipher_stream.write(header)
        except Exception as exc:
            raise exc # need to handle this specifically
        
    
    def write_packet(self, packet: bytearray):
        """Write the data into the cipher stream

        Args:
            packet: a bytearray contains data

        Returns:
            Nothing
        """
        data_len = struct.pack(">I",len(packet))
        try:
            self._cipher_stream.write(data_len)
             # confirm with Matt to make sure what this means
            self._cipher_stream.write(packet)
        except Exception as exc:
            raise exc