#
# def makeRegistrar():
#     registry = {}
#
#     def registrar(func):
#         registry[func.__name__] = func
#         return func
#
#     registrar.all = registry
#     return registrar
#
#
# class MyClass:
#     def __init__(self):
#         pass
#
#     command = makeRegistrar()
#
#     def run(self):
#         for key in self.command.all:
#             self.command.all[key](self)
#
#     @command
#     def f(self):
#         print('hello')
#
#     @command
#     def qwer(self):
#         print('qwer')
#
#
# a = MyClass()
# a.run()

#############################################################
# class Command:
#     functions = dict()
#
#     def __init__(self, command_type):
#         self.command_type = command_type
#
#     def __call__(self, func):
#         self.functions[self.command_type] = func
#         return func
#
#
#
#
# class MyClass:
#     def __init__(self):
#         pass
#
#     def run(self, name):
#         Command.functions[name](self)
#
#     @Command('hello_func')
#     def f(self):
#         print('hello')
#
#     @Command('qwer_func')
#     def qwer(self):
#         print('qwer')


# a = MyClass()
# a.run('hello_func')

####################################################
class Type:
    def __init__(self, name):
        self.__name = name

    def __hash__(self):
        return hash(self.__name)

    def __eq__(self, other):
        return self.__name == other.__name

    register = lambda self: self.__init__('register')


