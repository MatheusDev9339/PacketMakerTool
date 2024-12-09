from InquirerPy.validator import EmptyInputValidator
from InquirerPy import prompt
from Configs import configs
class Creation:
    directory_server = configs['directory_server']
    directory_client = configs['directory_client']
    all_processed = [
        'readBoolean', 'readBytes', 'readCompressedString', 'readLong', 'readString', 'readStringList', 'readVInt', 'readVIntList', 'writeBoolean', 
        'writeCompressedString', 'writeLong', 'writeString', 'writeStringList', 'writeVInt', 'writeVIntList']
    b_reads  = [item for item in all_processed if item.startswith('read')]
    b_writes = [item for item in all_processed if item.startswith('write')]
    def __init__(self, data):
        self.is_server = data['is_server']
        self.type = 'Server-Client' if self.is_server else 'Client-Server'
        self.class_name = data['class_name']
        self.class_number = data['class_number']
        self.data = data['data']
        self.run()
    def template_insert_server(self):
        lenght = len(self.data)
        resolved_name = self.class_name + 'Message'
        resolved_path = self.directory_server+resolved_name+'.py' if self.is_server else self.directory_client+resolved_name+'.py'
        try:
            file = open(resolved_path, 'x')
        except FileExistsError:
            pass
        n = '\n'
        file = open(resolved_path, '+a')
        file.write('from Classes.Packets.PiranhaMessage import PiranhaMessage' + n)
        file.write(f'class {resolved_name}(PiranhaMessage):' + n)
        file.write('    def __init__(self, messageData) -> None:' + n)
        file.write('        super().__init__(messageData)' + n)
        if self.is_server:
            file.write('    def encode(self, fields, player):' + n)
            for i in range(lenght):
                api = self.data[i]
                file.write(f'        self.{api['ByteStream']}(!) #{api['NameField']}' + n)
            file.write('    def decode(self):' + n)
            file.write('        fields = {}' + n)
            file.write('        return fields' + n)
        else:
            file.write('    def encode(self, fields, player):' + n)
            file.write('        pass' + n)
            file.write('    def decode(self):' + n)
            file.write('        fields = {}' + n)
            for i in range(lenght):
                api = self.data[i]
                file.write(f"""        fields['{api['NameField']}'] = self.{api['ByteStream']}()""" + n)
            file.write('        return fields' + n)
        file.writelines(['    def execute(self, conn, fields):' + n, '        pass' + n, '    def get_message_info(self):' + n, f'        return {self.class_number}' + n])
        print(f'Created {resolved_name} on {resolved_path}')
    def run(self):
        self.template_insert_server()
class Colette:
    def __init__(self):
        q = [{
        "type": "list",
        "message": "Message Type:",
        "choices": ['ServerMessage', 'ClientMessage'],
    },
    {
        "type": "number",
        "message": "How many Decodes:",
        "min_allowed": 0,
        "max_allowed": 256,
        "validate": EmptyInputValidator(),
    },
    {
        "type": "number",
        "message": "How many Encodes:",
        "min_allowed": 0,
        "max_allowed": 256,
        "validate": EmptyInputValidator(),
    },
    {"type": "input", "message": "Class name:"},
    {
        "type": "input",
        "message": "Class Code:",
    },
    ]
        data = {}
        result = prompt(questions=q[0])
        if result[0] == 'ServerMessage':
            data['is_server'] = True
            next_q = q[2]
        else:
            data['is_server'] = False
            next_q = q[1]
        data['class_name'] = prompt(q[3])[0]
        while True:
            try:
                clss_int = int(prompt(q[4])[0])
                break
            except:
                print('Valid number.')
                continue
        data['class_number'] = clss_int
        result = prompt(questions=next_q)
        data['data'] = []
        for i in range(int(result[0])):
            q = [
                {
        "type": "list",
        "message": f"On the {'Encode' if data['is_server'] else 'Decode'} of message {i+1} will be:",
        "choices": Creation.b_writes if data['is_server'] else Creation.b_reads},
                {
        "type": "input",
        "message": 'What will be sent? (# comment)' if data['is_server'] else 'Field name:',
        'default': 'No Comment' if data['is_server'] else ""
                },
                ]
            
            dataclass = prompt(q)
            data['data'].append({'ByteStream': dataclass[0], 'NameField': dataclass[1]})
        Creation(data)
Colette()
