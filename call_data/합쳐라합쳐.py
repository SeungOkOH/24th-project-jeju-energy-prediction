import tommorow_data_get
import torch
from predictions.elec_prediction import convert_elec
from predictions.solar_prediction import convert_solar
from predictions.wind_prediction import convert_wind

from models import Windpower_MLP, LSTMwithAttn

# GPU를 사용할 경우
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_energy_data():
    tomorrow_df = tommorow_data_get.get_data()

    elec_model_path = 'models/elec_model.pt'
    solar_model_path = 'models/solar_model.pt'
    wind_model_path = 'models/wind_model.pt'

    elec_model = LSTMwithAttn(input_dim=13, hidden_dim=64, output_dim=1, num_layers=2, device = DEVICE)
    elec_model.load_state_dict(torch.load(elec_model_path, map_location = 'cpu'))

    solar_model = LSTMwithAttn(input_dim=6, hidden_dim=64, output_dim=1, num_layers=2, device = DEVICE)
    solar_model.load_state_dict(torch.load(solar_model_path, map_location = 'cpu'))

    wind_model = Windpower_MLP()
    wind_model.load_state_dict(torch.load(wind_model_path, map_location = 'cpu'))

    features_test_elec = convert_elec(tomorrow_df.copy()).to(DEVICE)
    features_test_solar = convert_solar(tomorrow_df.copy()).to(DEVICE)
    features_test_wind = convert_wind(tomorrow_df.copy()).to(DEVICE)

    features_test_elec = features_test_elec.unsqueeze(0)
    features_test_solar = features_test_solar.unsqueeze(0)

    y_pred_elec = elec_model(features_test_elec)
    y_pred_solar = solar_model(features_test_solar)
    y_pred_wind = wind_model(features_test_wind)

    y_pred_elec = y_pred_elec.reshape(24)
    y_pred_solar = y_pred_solar.reshape(24)
    y_pred_wind = y_pred_wind.reshape(24)

    return {
        'elec': y_pred_elec.tolist(),
        'solar': y_pred_solar.tolist(),
        'wind': y_pred_wind.tolist()
    }

print(get_energy_data())