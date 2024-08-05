#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program converts temperature from Celsius to Fahrenheit and vice versa
    
    Python 3
    Author: Evan Aguilar
    Class: BIS 2330 - Computer programming II
    Date: 048/23/2024
"""

import eel
import collegeapp_controller

eel.init("web")


@eel.expose
def get_data():
    x = collegeapp_controller.grab("students")
    return x


@eel.expose
def send_data(role):
    print(role)


@eel.expose
def get_student_data():
    return collegeapp_controller.grab("students")


@eel.expose
def get_student_classes(student_data):
    print(student_data)
    student = {
        "id": student_data[0],
        "name": student_data[1],
        "email": student_data[2],
        "major": student_data[3],
    }

    return collegeapp_controller.process_student_schedule(student)


eel.start("index.html")
