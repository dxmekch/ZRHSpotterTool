#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 11:48:42 2019

@author: simon
"""

class FlightEntry:
    def __init__(self, entry=None):
        self.raw = entry
        if('flightcode' in entry):
            self.code = entry['flightcode']
        else:
            self.code = None
        self.reg = entry['masterflight']['registration']
        
    # Method override for == operator
    # compares registration and flightcode
    def __eq__(self, other):
        if isinstance(other, FlightEntry):
            if(self.code is not None and other.code is not None):
                # both Objects contain flilghtcode
                # their origin is not the dict file
                return ( self.code == other.code)
            else:
                # at least one Object does not have a flightcode
                # compare based on registration from the dict file
                return ( self.reg == other.reg)
        # TODO
        # implement comparison with strings
        # entry == 'HBJSK'
        # entry == 'XXE 1725'
        return NotImplemented
    
