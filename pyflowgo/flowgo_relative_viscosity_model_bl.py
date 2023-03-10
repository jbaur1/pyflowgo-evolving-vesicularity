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

import math
import json
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_vesicle_fraction_model_bimodal

import pyflowgo.base.flowgo_base_relative_viscosity_model

import pyflowgo.flowgo_material_lava


class FlowGoRelativeViscosityModelBirnbaumLev(pyflowgo.base.flowgo_base_relative_viscosity_model.
                                                 FlowGoBaseRelativeViscosityModel):
    """This methods permits to calculate the effect of crystals and bubbles cargo on viscosity according to
    Birnbaum and Lev. They propose a treatment for the viscosity of a three‐phase mixture
    comprising a suspension of rigid particles and bubbles based on analogue experiments.
    The input parameters include the crystal fraction (phi) and the bubbles fraction (vesicle_fraction retrieved 
    from the vesicle_fraction_model) """

    def __init__(self, vesicle_fraction_model=None, melt_viscosity_model=None):
        super().__init__()

        if vesicle_fraction_model == None:
            self._vesicle_fraction_model = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        else:
            self._vesicle_fraction_model = vesicle_fraction_model

        if melt_viscosity_model == None:
            self._melt_viscosity_model = pyflowgo.flowgo_melt_viscosity_model_shaw.FlowGoMeltViscosityModelShaw()
        else: 
            self._melt_viscosity_model = melt_viscosity_model

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._phimax = float(data['relative_viscosity_parameters']['max_packing'])
            self._beinstein = float(data['relative_viscosity_parameters']['einstein_coef'])
            self._strainrate = float(data['relative_viscosity_parameters']['strain_rate'])

    def compute_relative_viscosity(self, state):
        phi = state.get_crystal_fraction()
        #the vesicle model is directly called
        vesicle_fraction = self._vesicle_fraction_model.computes_vesicle_fraction(state)
        melt_viscosity = self._melt_viscosity_model.compute_melt_viscosity(state)

        n = 1
        if (phi + vesicle_fraction)>=0.39:
            Ca = 0.01*self._strainrate*melt_viscosity/0.37
            n = 1 + (0.7 - 0.55*Ca) * (0.39 - phi - vesicle_fraction)

        relative_viscosity = (1. - (phi / (self._phimax*(1. - vesicle_fraction)))) ** (-2.94) * \
                             (1. - vesicle_fraction) ** (-self._beinstein) * ((self._strainrate) ** (n - 1))

        return relative_viscosity

    def is_notcompatible(self, state):
        phi = state.get_crystal_fraction()
        vesicle_fraction = self._vesicle_fraction_model.computes_vesicle_fraction(state)

        if phi > (self._phimax*(1 - vesicle_fraction)):
            return True
        else:
            return False