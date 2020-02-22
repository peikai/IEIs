from pymatgen import Composition, Element
import pandas as pd
import numpy as np


chemsys_multiple = pd.read_csv('tables/Na/chemsys_all.csv', usecols=['chemsys']).values
pure_materials = pd.read_csv('tables/pure_element_materials.csv', usecols=['pretty_formula']).values

# remove duplicated elements and polymorphic compounds
chemsys_list = np.hstack(chemsys_multiple)
element_array = np.hstack([chemsys.split('-') for chemsys in chemsys_list])
chemsys_elements = np.unique(element_array)
pure_materials = np.unique(pure_materials)

pure_material_elements = set(Composition(material).elements.pop() for material in pure_materials)

element_omitted = np.hstack([element.name for element in pure_material_elements if element.name not in chemsys_elements])
# omit noble gas
# may need to omit noble gas
# boolean = [element.is_noble_gas for element in pure_material_omitted_elements]
# pure_material_omitted_candidate = pure_material_omitted[boolean]

chemsys_binary = pd.DataFrame(['Na-' + element for element in element_omitted], columns=['chemsys'])
chemsys_binary.to_csv('chemsys_binary.csv', index=False)
