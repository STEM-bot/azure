import re

class Listener():
    def __init__(self, kernel):
        self.text = ''
        self.ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        self.img_data = None
        self.kernel = kernel

    def escape_ansi_text(self):
        return self.ansi_escape.sub('', self.text)

    def output_cb(self, msg):
        msg_type = msg['msg_type']
        content = msg['content']
        if msg_type == 'execute_result': # or msg_type == 'display_data':
            self.text += content['data']['text/plain']
        elif msg_type == 'display_data' and self.kernel == 'r' and 'text/plain' in content['data']:
            if content['data']['text/plain'] != 'plot without title':
                self.text += content['data']['text/plain']
        elif msg_type == 'stream':
            self.text += content['text']
        elif msg_type == 'error':
            for line in content['traceback']:
                self.text += line
                self.text += '\n'
        if 'data' in content and 'image/png' in content['data']:
            self.img_data = content['data']['image/png']
        else:
            pass