# EasyJ
## EasyJ is a python application designed to quickly create Java templates with an inheritance diagram.

EasyJ is a python utility to speed up the process of writing Java code.
EasyJ aims to create an interface in which the user can customize and declare java classes
The user will be able to visually route inheritance between classes, and will be able to declare interfaces
The user will also be able to sketch out methods for classes with all the details.

EasyJ defines a class "Class" (a little confusing, I know) that has two children.
Each EasyJ project only allows for a singular instance of a parentClass.
Hence, it is coded as a singleton.
subClasses are child Classes. They must have a defined parent of type Class.
All Classes have a name, and access modifier, a type, and the option of a main method.
All Classes have the ability to implement multiple interfaces

EasyJ has its own defined exceptions it will throw when the situation calls for it
