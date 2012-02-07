class Enum(object):

    #HASNT_RUN = 0
    #SUCCESS = 1
    #FAIL = 2
    #PARTIAL = 3

    def __init__(self, enum_list):
        self.enum_list = enum_list.split(' ')
        for i, e in enumerate(self.enum_list):
            setattr(self, e, i)

    def string(self, value):
        return self.enum_list[value]

status = Enum('HASNT_RUN SUCCESS FAIL PARTIAL')
