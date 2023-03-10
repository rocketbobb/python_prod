# python_prod

python_prod - version 0.1

Best practices for building production python applications

"""python_prod

Work in progress to define a collection of best practices, functions, wrappers, and utilities designed to help produce python code that is "production ready". 

Production ready is defined to build code that enforces consistent argument overrides, provides a standardized logging pattern for application log records, provides simple means to test new utilities, and defines a separate method and standardized format to handle application exceptions.

Current items include:

common-best-practices.py - main program
config.py - config
OS shell wrapper ( Bash/Zsh )

lib/exceptions.py - example of exception class
lib/set_env.py - code to capture and access python environment variables
lib/args.py - basic example of using python argument package, honoring precedence rules of cmd line args, before enviornment, before internal defaults.
lib/utils.py - various helper utilities

Also of note, all library and utility packages contain a main to faciliate the execution and testing of the utilities seperate from the application
"""