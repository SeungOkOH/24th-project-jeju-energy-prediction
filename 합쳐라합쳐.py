import tommorow_data_get
import dataset_define
import torch

data_origin = tommorow_data_get.get_data()

elec_model_path = '/models/elec_model.pt'
solar_model_path = '/models/solar_model.pt'
wind_model_path = '/models/wind_model.pt'

elec_model = torch.load(elec_model_path)
solar_model = torch.load(solar_model_path)
wind_model = torch.load(wind_model_path)

elec = elec_model(data)
solar = solar_model(data_solar)
wind = wind_model(data_wind)