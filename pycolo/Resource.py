# -*- coding:utf-8 -*-

class Resource:

    def __init__(self):
        """
        If a Core Link description string is passed, the resource created match the description
        given by this string.
        """
        raise "Not implemented yet"

    def changed(self):
        """
        Send a notification to all the subscribed resource.
        """
        raise "Not implemented yet"

    def to_link(self, recursive=False):
        """
        Return a Core Link representation of the resource and all sub-resources.
        """

        if recursive:
            raise "Not implemented yet"

    def __len__(self):
        return len(self.__dict__)

    def count(self, recursive=False):
        if recursive:
            raise "Not implemented yet"
        else:
            len(self)

    def __str__(self):
        return "Not implemented yet"