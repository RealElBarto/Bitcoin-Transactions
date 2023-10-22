from format_converter import Converter
from helper_functions import read_varint, encode_varint
from op import OP_CODE_NAMES


converter = Converter()


def p2pkh_script(hash160: str) -> "Script":
    
    return Script([0x76, 0xa9, hash160, 0x88, 0xac])


class Script:

    def __init__(self, commands=None):
        if commands is None:
            self.commands = []
        else:
            self.commands = commands


    def __repr__(self) -> str:
        result = []
        for command in self.commands:
            if type(command) == int:
                if OP_CODE_NAMES.get(command):
                    name = OP_CODE_NAMES.get(command)
                else:
                    name = 'OP_[{}]'.format(command)
                result.append(name)
            else:
                result.append(command.hex())
        return ' '.join(result)


    @classmethod
    def parse(cls, stream: bytes) -> "Script":
        length = read_varint(stream)
        commands = []
        count = 0
        while count < length:
            current = stream.read(1)
            count += 1
            current_byte = current[0]
            if current_byte >= 1 and current_byte <= 75:
                n = current_byte
                commands.append(stream.read(n))
                count += n
            elif current_byte == 76:
                data_length = converter.little_endian_to_int(stream.read(1))
                commands.append(stream.read(data_length))
                count += data_length + 1
            elif current_byte == 77:
                data_length = converter.little_endian_to_int(stream.read(2))
                commands.append(stream.read(data_length))
                count += data_length + 2
            else:
                op_code = current_byte
                commands.append(op_code)
        if count != length:
            raise SyntaxError('parsing script failed')
        
        return cls(commands)
    

    def serialize(self) -> str:
        script = b''
        for command in self.commands:
            if type(command) == int:
                script += converter.int_to_little_endian(command, 1)
            else:
                length = len(command)
                if length < 75:
                    script += converter.int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:
                    script += converter.int_to_little_endian(76, 1)
                    script += converter.int_to_little_endian(length, 1)
                elif length >= 0x100 and length <= 520:
                    script += converter.int_to_little_endian(77, 1)
                    script += converter.int_to_little_endian(length, 2)
                else:
                    raise ValueError('too long an command')
                script += command

        total = len(script)

        return encode_varint(total) + script