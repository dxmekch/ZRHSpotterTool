#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 11:48:42 2019

@author: simon
"""

class FlightEntry:
    def __init__(self, entry=None):
        self.raw = entry
        # self.flightcode = entry['flightcode']
        self.reg = entry['masterflight']['registration']
        
    # Method override for == operator
    # compares registration and flightcode
    def __eq__(self, other):
        if isinstance(other, FlightEntry):
            # comparison is based on registration
            return ( self.reg == other.reg)
        # TODO
        # implement comparison with strings
        # entry == 'HBJSK'
        # entry == 'XXE 1725'
        return NotImplemented
    
