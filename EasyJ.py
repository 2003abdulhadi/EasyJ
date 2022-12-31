from abc import abstractmethod
from io import TextIOWrapper
from typing import final

"""
EasyJ - by Abdul Hadi

EasyJ is a python utility to speed up the process of writing Java code.
EasyJ aims to create an interface in which the user can customize and declare java classes
The user will be able to visually route inheritance between classes, and will be able to declare interfaces
The user will also be able to sketch out methods for classes with all the details.

Last Updated: 14/11/22
To do:
    - Test parameterization on implementing interfaces
    - Reduce redundancy
    - Implement Enum for access modifiers, method and class and variables types (final, abstract, static, etc.)
    - Implement quick code for getters and setters
    - Implement abstract, final and static errors
    - Bug fix!!!
"""
#your an idiot who fogot how java works and need to correct the part where you
#incorrectly assgined access modifiers to classes instead of subclasses and methods and such

# ----------------------------------------------------------------------------------------- back end -----------------------------------------------------------------------------------------
"""
The following code is used to script the back end of EasyJ.
EasyJ defines a class "Class" (a little confusing, I know) that has two children.
                      ^^ case sensitive
Each EasyJ project only allows for a singular instance of a parentClass.
Hence, it is coded as a singleton.
subClasses are child Classes. They must have a defined parent of type Class.
All Classes have a name, and access modifier, a type, and the option of a main method.
All Classes have the ability to implement multiple interfaces

EasyJ has its own defined exceptions it will throw when the situation calls for it
"""

class Variable():

    def __init__(self, name: str, type: str, array_dimension: int = 0) -> None:

        self.instanceChecks(name, type, array_dimension)

        self.name = name
        self.type = type
        self.array_dimension = array_dimension

    def instanceChecks(self, name, type, array_dimension):
        for attr in [name, type]:
            if not (isinstance(attr, str)):
                raise TypeError(f'Parameter {attr} must be of type: str')

        if not isinstance(array_dimension, int):
            raise TypeError(f'Parameter {array_dimension} must be of type: int')

    def __str__(self) -> str:
        return f'{self.type}{self.array_dimension*"[]"} {self.name}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' + ', '.join([f'self.{attr}={vars(self)[attr]}' for attr in vars(self)]) + f') at {hex(id(self))}'

class Method():

    def __init__(self, name: str, returns: str = 'void', parameters: list[Variable] = Variable('','')) -> None:
        
        self.instanceChecks(name, returns, parameters)

        self.returns = returns
        self.name = name
        self.paramaters = parameters

        self.formatVars()

    def instanceChecks(self, name, returns, parameters):
        for attr in [name, returns]:
            if not (isinstance(attr, str)):
                raise TypeError(f'Parameter {attr} must be of type: str')

        if not (isinstance(parameters, (list, Variable))):
            raise TypeError(f'Parameter {parameters} must be of type: lst OR Variable')

        if not (isinstance(parameters, Variable)):
            for attr in parameters:
                raise TypeError(f'Parameter {attr} must be of type: Variable')

    def formatVars(self):
        for attr in vars(self):
            if (isinstance(getattr(self, attr), str)):
                setattr(self, attr, vars(self)[attr].strip())
        
        if isinstance(self.paramaters, Variable):
            self.paramaters = [self.paramaters]


    def __str__(self) -> str:

        string = ''
        _ = [getattr(self, attr) for attr in vars(self) if type(getattr(self, attr)) is not list]

        while '' in _:
            _.remove('')
        string += ' '.join(_)

        _ = [params.__str__() for params in self.paramaters]
        string += ' (' + ', '.join(_) + ')'

        return string
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' + ', '.join([f'self.{attr}={vars(self)[attr]}' for attr in vars(self)]) + f') at {hex(id(self))}'

class Class():    

    # starting java file
    java_file = ''

    def __init__(self, name: str) -> None:
        self.instanceChecks(name)

        self.name = name

        self.openFile()

    def instanceChecks(self, name):
        for attr in [name]:
            if not (isinstance(attr, str)):
                raise TypeError(f'Parameter {attr} must be of type: str')

    
    # method to open and start writing to a file
    @final
    def openFile(self):
        self.java_file = open(f'{self.name}.java', 'w')

    # method to close the file
    @final
    def closeFile(self):
        self.java_file.close()

    @final
    def completeFile(self):
        self.closeFile()

    # class decleration method that every child of Class must implement
    @abstractmethod
    def __str__(self) -> str:
        pass

    @final
    def getName(self):
        return self.name
    
    @final
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' + ', '.join([f'self.{attr}={vars(self)[attr]}' for attr in vars(self)]) + f') at {hex(id(self))}'

class ParentClass(Class):

    instance = None

    @staticmethod
    def get_instance():
        if ParentClass.instance is None:
            ParentClass()
        return ParentClass.instance
        
    def __init__(self, name: str) -> None:
        if ParentClass.instance is None:
            ParentClass.instance = self 
            super().__init__(name)
            self.completeFile()

    def __str__(self) -> str:

        string = ''
        _ = [getattr(self, attr) for attr in vars(self) if type(getattr(self, attr)) is not TextIOWrapper]
        
        _.insert(0, 'class')
        while '' in _:
            _.remove('')
        string += ' '.join(_)

        return string

class SubClass(Class):
        
    def __init__(self, name: str, parent: Class) -> None:
        super().__init__(name)
        self.parent = parent
        self.completeFile()

    def __str__(self) -> str:

        string = ''
        _ = [getattr(self, attr) for attr in vars(self) if type(getattr(self, attr)) is not TextIOWrapper]

        _.insert(0, 'class')
        while '' in _:
            _.remove('')
        _[2] = _[2].getName()
        _.insert(2, 'extends')
        string += ' '.join(_)

        return string

# class for ClassErrors, contains all exceptions related to Class creation
class ClassErrors(Exception):

    class NameFormatError(Exception):
        def __init__(self, name: str) -> None:
            self.name = name
            super().__init__()

        def __str__(self) -> str:
            return f'class name ({self.name}) can not contain spaces'
    
    class InvalidModifierError(Exception):
        def __init__(self, modifier: str, cls, valid_options: list[str]) -> None:
            self.modifier = modifier
            self.cls = cls
            self.valid_options = valid_options
            super().__init__()

        def __str__(self) -> str:
            return f'{self.cls} has no modifier ({self.modifier}. Only {self.valid_options.keys()} are allowed as modifiers)'

    class BackwardsAccessError(Exception):
        def __init__(self, child: Class, parent: Class) -> None:
            self.child = child
            self.parent = parent
            super().__init__()

        def __str__(self) -> str:
            return f'Class {self.parent.name}({self.parent.access_modifier.strip()}) has more restircted access than its child {self.child.name} ({self.child.access_modifier.strip()})'

    class ExtendedFinalError(Exception):
        def __init__(self, cls) -> None:
            self.cls = cls

        def __str__(self) -> str:
            if isinstance(self.cls, Class):
                return f'Can not extend final class {self.cls.name}'
            if isinstance(self.cls, Method):
                return f'Can not overwrite final method {self.cls.name}'

def main():

    v1 = Variable("args", 'String', 1)
    m1 = Method('main', parameters=v1)
    c1 = ParentClass('Parent')
    c2 = SubClass('Child', c1)
    print(v1.__repr__())
    print(m1.__repr__())
    print(c1.__repr__())
    print(c2.__repr__())
    print(v1)
    print(m1)
    print(c1)
    print(c2)


if __name__ == "__main__":

    main()