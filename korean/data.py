# -*- coding: utf-8 -*-
"""
    korean.data
    ~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import json
import os

from .morphology.particle import Particle


def load_data():
    with open(os.path.join(os.path.dirname(__file__), 'data.json')) as f:
        data = json.load(f)
    # register allomorphic particles
    for forms in data['allomorphic_particles'].itervalues():
        particle = Particle(*forms)
        for form in forms:
            Particle.register(form, particle)


load_data()
