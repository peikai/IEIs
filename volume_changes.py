from pymatgen.analysis.phase_diagram import PDEntry, PDPlotter, PhaseDiagram
from pymatgen.apps.battery.battery_abc import (AbstractElectrode,
                                               AbstractVoltagePair)
from pymatgen.apps.battery.conversion_battery import ConversionElectrode
from pymatgen.core.composition import Composition
from pymatgen.ext.matproj import MPRester
import numpy as np
from pandas import DataFrame

# find compounds in elements.
# element_list = ['Zn','Ag','Li']
element_list = ['I', 'F', 'Li']
# element_list = ['Al', 'Ni', 'Li']


with MPRester(api_key="25wZTKoyHkvhXFfO") as mpr:
    # find stable compounds consisted of given elements. Here needs ComputedStructureEntries
    entries = mpr.get_entries_in_chemsys(element_list, inc_structure='final')

pd = PhaseDiagram(entries)
stable_entries = [e.entry_id for e in pd.stable_entries]

# give quieries for (final relaxed volume of the material, gravimetric capacity) of each compounds
volume_query = mpr.query(criteria={'material_id':{'$in':stable_entries}}, properties=['material_id', 'pretty_formula', 'volume'])
volume_dict = DataFrame(volume_query)
print(volume_dict)

# comp = Composition("Al3Ni")
comp = Composition("IF7")

# electrode = ConversionElectrode.from_composition_and_pd(comp, pd)
electrode = ConversionElectrode.from_composition_and_entries(comp, entries)
# get voltage_pairs to acquire volumes
voltage_pairs = electrode.voltage_pairs
# discharge volume may often larger than charged volume, unless phase transitions occurred
volume_list = [(e.vol_charge, e.vol_discharge) for e in voltage_pairs]
volume_change_onestep = np.array([(e.vol_discharge/e.vol_charge - 1) for e in voltage_pairs])
# accumulate volume change at a certain step
volume_change_cumsum = np.cumsum(volume_change_onestep)

capacity_onestep = np.array([e.mAh for e in voltage_pairs])
rxn_onestep = np.array([e.rxn for e in voltage_pairs])
voltage_onestep = np.array([e.voltage for e in voltage_pairs])

# max. volume - min. volume
max_delta_volume = electrode.max_delta_volume

print(volume_list)
# print(volume_change_cumsum)
# print(capacity_onestep)
print(rxn_onestep)
# print(voltage_onestep)
# print(max_delta_volume)
# print(get_element_profile()

# print(electrode.get_sub_electrodes(adjacent_only=True))

# print(electrode.get_summary_dict())

# plotter = PDPlotter(pd)
# plotter.show()
# # Zn2Ag
# query = m.get_data('mp-1093999', prop='volume').pop()
# material_id, volume = query.values()
# # ZnAg
# volume2 = m.get_data('mp-1187974', prop='volume')
# print(volume2)
# # ZnAg3
# volume3 = m.get_data('mp-1187952', prop='volume')
# print(volume3)
# # 

# pd = PhaseDiagram(entries)
# stable_entries = [e.entry_id for e in pd.stable_entries]
# print(stable_entries)

# give quieries for (final relaxed volume of the material, gravimetric capacity) of each compounds
# volume_dict = mpr.query(criteria={'material_id':{'$in':stable_entries}}, properties=['material_id', 'volume'])
# print(volume_dict)
