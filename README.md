# python_prod

python_prod

Best practices for building production python applications

"""python_prod

Work in progress to define a collection of best practices, funcations, wrappers and utilities designed to help produce python code that is "production ready"

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