# Copyright 2017 PyFLOWGO development team (Magdalena Oryaelle Chevrel and Jeremie Labroquere)
#
# This file is part of the PyFLOWGO library.
#
# The PyFLOWGO library is free software: you can redistribute it and/or modify
# it under the terms of the the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# The PyFLOWGO library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received copies of the GNU Lesser General Public License
# along with the PyFLOWGO library.  If not, see https://www.gnu.org/licenses/.

import json
import math

import pyflowgo.base.flowgo_base_vesicle_fraction_model


class FlowGoVesicleFractionModelPoly(pyflowgo.base.flowgo_base_vesicle_fraction_model.
                                        FlowGoBaseVesicleFractionModel):

    # For Kilauea 2018

    _vesicle_fraction_1 = 0.7415
    _vesicle_poly_a = -0.0014
    _vesicle_poly_b = -0.0216


    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)

            if 'vesicle_fraction_1' not in data['lava_state']:
                raise ValueError("Missing ['lava_state']['vesicle_fraction_1'] entry in json")

            if 'vesicle_poly_a' not in data['lava_state']:
                raise ValueError("Missing ['lava_state']['vesicle_poly_a'] entry in json")

            if 'vesicle_poly_b' not in data['lava_state']:
                raise ValueError("Missing ['lava_state']['vesicle_poly_b'] entry in json")

            self._vesicle_fraction_1 = float(data['lava_state']['vesicle_fraction_1'])
            self._vesicle_poly_a = float(data['lava_state']['vesicle_poly_a'])
            self._vesicle_poly_b = float(data['lava_state']['vesicle_poly_b'])


    def computes_vesicle_fraction(self, state):
        current_position = state.get_current_position()

        return self._vesicle_poly_a*math.pow((current_position/1000),2) + self._vesicle_poly_b*(current_position/1000) + self._vesicle_fraction_1


# add stopping value T 0 vesicularity
