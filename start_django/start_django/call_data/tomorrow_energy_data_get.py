from .tommorow_data_get import get_data
import torch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from .predictions.elec_prediction import convert_elec
from .predictions.solar_prediction import convert_solar
from .predictions.wind_prediction import convert_wind

from models import Windpower_MLP, LSTMwithAttn

# GPU를 사용할 경우
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def find_project_dir():
    current_dir = os.getcwd()
    # 현재 디렉토리에서 시작하여 '24th-project-jeju-energy-prediction'을 찾고,
    # 그 안의 'start_django\start_django' 경로를 확인합니다.
    while True:
        if os.path.basename(current_dir) == '24th-project-jeju-energy-prediction':
            # '24th-project-jeju-energy-prediction' 디렉토리 내부의 'start_django\start_django' 경로를 확인합니다.
            start_django_path = os.path.join(current_dir, 'start_django', 'start_django')
            if os.path.exists(start_django_path):
                return start_django_path  # 이 경로가 존재한다면 반환합니다.
            else:
                raise FileNotFoundError("The start_django\\start_django directory was not found.")
        current_dir = os.path.dirname(current_dir)
        if current_dir == os.path.dirname(current_dir):  # 더 이상 상위 디렉토리가 없을 때
            return None
        
def get_energy_data():
    tomorrow_df = get_data()
    
    project_dir = find_project_dir()
    if project_dir is None:
        raise FileNotFoundError("The project directory was not found in the current directory tree.")
    call_data_dir = os.path.join(project_dir, 'call_data')  # 올바른 경로를 설정
    os.chdir(call_data_dir)  # 작업 디렉토리 변경


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