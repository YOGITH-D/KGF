import joblib
cat_model=joblib.load('cat_model.pkl')

def make_prediction(input_list):
    starch_flow = input_list[2]     
    amina_flow = input_list[3]      
    ore_pulp_flow = input_list[4]

    iron_conc = 65.04756905402098
    starch_to_pulp = starch_flow / ore_pulp_flow if ore_pulp_flow != 0 else 0
    amina_to_pulp = amina_flow / ore_pulp_flow if ore_pulp_flow != 0 else 0
    print('input list', len(input_list))
    complete_list = input_list + [iron_conc,starch_to_pulp, amina_to_pulp]
    prediction=cat_model.predict([complete_list])
    return prediction


low_silica_example =[
    68.0,   # % Iron Feed
    1.8,    # % Silica Feed
    3600.0, # Starch Flow
    550.0,  # Amina Flow
    400.0,  # Ore Pulp Flow
    10.0,   # Ore Pulp pH
    1.7,    # Ore Pulp Density
    290.0,  # Flotation Column 01 Air Flow
    295.0,  # Flotation Column 02 Air Flow
    300.0,  # Flotation Column 03 Air Flow
    305.0,  # Flotation Column 04 Air Flow
    310.0,  # Flotation Column 05 Air Flow
    315.0,  # Flotation Column 06 Air Flow
    320.0,  # Flotation Column 07 Air Flow
    540.0,  # Flotation Column 01 Level
    545.0,  # Flotation Column 02 Level
    550.0,  # Flotation Column 03 Level
    435.0,  # Flotation Column 04 Level
    440.0,  # Flotation Column 05 Level
    445.0,  # Flotation Column 06 Level
    450.0,  # Flotation Column 07 Level
]


high_silica_example = [
    42.0,   # % Iron Feed
    32.0,   # % Silica Feed
    1800.0, # Starch Flow
    350.0,  # Amina Flow
    370.0,  # Ore Pulp Flow
    9.2,    # Ore Pulp pH
    1.55,   # Ore Pulp Density
    260.0,  # Flotation Column 01 Air Flow
    265.0,  # Flotation Column 02 Air Flow
    270.0,  # Flotation Column 03 Air Flow
    275.0,  # Flotation Column 04 Air Flow
    280.0,  # Flotation Column 05 Air Flow
    285.0,  # Flotation Column 06 Air Flow
    290.0,  # Flotation Column 07 Air Flow
    310.0,  # Flotation Column 01 Level
    315.0,  # Flotation Column 02 Level
    320.0,  # Flotation Column 03 Level
    300.0,  # Flotation Column 04 Level
    305.0,  # Flotation Column 05 Level
    310.0,  # Flotation Column 06 Level
    315.0,  # Flotation Column 07 Level
]


prediction=make_prediction(low_silica_example)
print(f'{prediction[0]} => low silica')
prediction=make_prediction(high_silica_example)
print(f'{prediction[0]} => high silica')