import Tkinter
import threading
import Queue
import logging

from main import run_checks
from write_vpn_config import write_config


class GUI(Tkinter.Frame):
    def __init__(self, queue, master=None):
        self.queue = queue
        super(GUI, self).__init__(master)
        self.grid()
        self.create_widgets()
        self.check_queue()

    def create_widgets(self):
        self.scrollbar = Tkinter.Scrollbar(self, orient='vertical')
        self.text = Tkinter.Text(self, width=80, height=25, state='disabled',
                                 yscrollcommand=self.scrollbar.set)
        self.scrollbar['command'] = self.text.yview
        self.write_vpn_button = Tkinter.Button(self,
                                               command=self.write_vpn_config,
                                               text="Write VPN Config")
        self.quit_button = Tkinter.Button(self, command=self.quit, text="Quit")
        self.text.grid(row=0, columnspan=2)
        self.scrollbar.grid(row=0, column=2, sticky='ns')
        self.write_vpn_button.grid(row=1, sticky='w')
        self.quit_button.grid(row=1, column=1, sticky='e')

    def check_queue(self):
        while True:
            try:
                msg = queue.get_nowait()
            except Queue.Empty:
                break
            else:
                self.text['state'] = 'normal'
                self.text.insert('end', msg)
                self.text['state'] = 'disabled'
                self.text.see('end')
                queue.task_done()

        self.after(100, self.check_queue)

    def write_vpn_config(self):
        write_config()


class MyHandler(logging.Handler):
    def __init__(self, queue):
        self.queue = queue
        super(MyHandler, self).__init__()

    def emit(self, record):
        queue.put(record.getMessage() + '\n')


if __name__ == '__main__':
    queue = Queue.Queue()

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.addHandler(MyHandler(queue))

    gui = GUI(queue)
    gui.master.title("HiSPARC diagnostics")

    job = threading.Thread(target=run_checks)
    job.daemon = True
    job.start()

    gui.mainloop()
