import os
import win32com.client as win32


class ASPENConnector:
    def __init__(self, base_path):
        self.base_path = base_path
        self.app_name = "Apwn.Document"

    def __dispatch__(self):
        self.aspen = win32.Dispatch(self.app_name)

    def __open_system(self):
        self.aspen.InitFromArchive2(os.path.abspath(self.base_path))
        self.aspen.Visible = 1
        self.aspen.SuppressDialogs = 1
        self.aspen.Engine.Run2()

    def connect(self):
        self.__dispatch__()
        self.__open_system()

