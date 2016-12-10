from . import connection
from . import executable

import time

class Room(executable.Executable):
    """
    A base room object that simply holds a connection and simple methods for
    interfacing with the room.
    """

    def __init__(self, roomname, password=None, attempts=None):
        super().__init__()

        self.connection = connection.Connection()

        self.roomname = roomname
        self.password = password

        self.nickname = None

        self.attempts = attempts

    def join(self):
        """
        join() -> Bool

        Connects to the room and sends the passcode.
        """

        ret = False

        if self.connection is not None:
            ret = self.connection.connect(self.roomname)
            if ret:
                if self.password is not None:
                    self.connection.send_packet("auth",
                        dict(type="passcode", passcode=self.password))

        return ret

    def identify(self):
        """
        identify() -> None

        Identifies with the server according to the nickname.
        """

        if self.connection is not None:
            if self.nickname is not None:
                self.connection.send_packet("nick", dict(name=self.nickname))

    def quit(self):
        """
        quit() -> None

        Performs neccessary cleanup for the connection.
        """

        self.cleanup()

        if self.connection is not None:
            self.connection.close()

        super().quit()

    def jump(self, room):
        """
        jump() -> Bool

        Jump to another room.
        """

        ret = self.connection.refresh(room)
        self.identify()

        return ret

    def ready(self):
        """
        ready() -> None

        Overrideable function that is called every time the room is ready for
        transmitting information.
        """

        pass

    def cleanup(self):
        """
        cleanup() -> None

        Overrideable cleanup function that is called when the room is closing.
        """

        pass

    def run(self):
        """
        run() -> None

        Run the room.
        """

        super().run()

        first_attempt = True
        attempts = 0

        while self.running:
            #Check for multiple failures in a row
            if self.attempts is not None and attempts >= self.attempts:
                self.quit()
                break

            #Receive data and handle connection errors
            try:
                if self.connection.receive_data():
                    attempts = 0
                else:
                    #No connection initialized
                    if first_attempt:
                        first_attempt = False
                    else:
                        #Just disconnected
                        if attempts == 0:
                            self.cleanup()

                        attempts += 1
                        time.sleep(5 ** attempts)

                    self.join()
                    self.identify()
                    self.ready()
            #Catching some exception that occurs in single threading bots
            except OSError:
                break
