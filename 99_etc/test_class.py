class ABCD():
    aa = 1
    def __init__(self):
        self.bb = 2
    @classmethod
    def class_method(cls):
        cls.aa += 1
        print(cls.aa)
        # print(cls.bb)
    @staticmethod
    def static_method():
        print("this is staticmethod")

ABCD.class_method()
ABCD.class_method()
ABCD.class_method()
ABCD.class_method()

class ABCD():
    aa = 1
    def __init__(self):
        self.bb = 2
    @classmethod
    def class_method(cls):
        cls.aa += 1
        print(cls.aa)
        # print(cls.bb)
    @staticmethod
    def static_method():
        print("this is staticmethod")

print(ABCD.aa)
