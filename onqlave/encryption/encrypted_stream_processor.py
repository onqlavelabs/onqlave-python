import io

from onqlave.keymanager.onqlave_types.types import AlgorithmDeserialiser

class EncryptedStreamProcessor:
    """A stream processor for the encrypted stream in the decryption process
    with two functions including reading the header and reading the packet.    
    """
    def __init__(self, cipher_stream: io.BytesIO) -> None:
        """Init an EncryptedStreamProcessor object which takes the cipher
        stream in the decryption process as its main attribute

        Args:
            cipher_stream: a standard python stream object

        Returns:
            Nothing
        """
        self._cipher_stream = cipher_stream

    def read_header(self):
        """Read the header of the cipher stream into a bytearray with length of 4,
        then extract the algorithm infromation packed in the header

        Args:
            Nothing

        Returns:
            The information of algorithm packed in the header, as an AlgorithmDeserialiser object
        """
        header_len_buffer = bytearray(4)
        data_len = self._cipher_stream.readinto(header_len_buffer)

        if data_len < 4:
            return None # invalid cipher data
        
        header_len = int.from_bytes(header_len_buffer,byteorder='big')
        header_buffer = bytearray(header_len - 4)
        
        data_len = self._cipher_stream.readinto(header_buffer)
        
        if data_len < header_len - 4:
            return None # invalid cipher data
        
        algorithm = AlgorithmDeserialiser()
        algorithm.deserialise(buffer=header_len_buffer + header_buffer)

        return algorithm
    
    def read_packet(self):
        """Read the data in the packet of the cipher stream

        Args:
            Nothing

        Returns:
            A bytearray contains the data in the packet of the cipher stream
        """
        packet_len_buffer = bytearray(4)
        try:
            data_len = self._cipher_stream.readinto(packet_len_buffer)
        except Exception:
            return None
        
        if data_len < 4:
            return None # invalid cipher data
        
        packet_len = int.from_bytes(packet_len_buffer,'big')
        buffer = bytearray(packet_len)
        data_len = self._cipher_stream.readinto(buffer)

        if data_len < int(packet_len):
            return None # invalid cipher data
        
        return buffer