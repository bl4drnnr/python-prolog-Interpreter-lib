class Error(Exception):
    pass


class SingleArgument(Error):
    pass


class WrongOption(Error):
    pass


class WrongJsonFormat(Error):
    pass


class WrongFactFormat(Error):
    pass


class WrongPrologFormat(Error):
    pass
