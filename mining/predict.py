import joblib
cat_model=joblib.load('cat_model.pkl')

def make_prediction(input_list):
    starch_flow = input_list[2]     
    amina_flow = input_list[3]      
    ore_pulp_flow = input_list[4]

    iron_conc = 65.04756905402098
    starch_to_pulp = starch_flow / ore_pulp_flow if ore_pulp_flow != 0 else 0
    amina_to_pulp = amina_flow / ore_pulp_flow if ore_pulp_flow != 0 else 0

    complete_list = input_list + [iron_conc, starch_to_pulp, amina_to_pulp]
    prediction=cat_model.predict([complete_list])
    return prediction


low_silica_example = [
    69.5,   # % Iron Feed (very high)
    2.5,    # % Silica Feed (very low)
    750,    # Starch Flow
    200,    # Amina Flow
    1150,   # Ore Pulp Flow
    10.8,   # Ore Pulp pH (slightly alkaline, good separation)
    1.35,   # Ore Pulp Density
    750, 720, 740, 710, 690, 705, 715,   # Air Flows (balanced)
    9.2, 9.5, 9.3, 9.1, 9.4, 9.6, 9.3    # Levels (stable)
]

prediction=make_prediction(low_silica_example)
print(f'{prediction[0]} => low silica')