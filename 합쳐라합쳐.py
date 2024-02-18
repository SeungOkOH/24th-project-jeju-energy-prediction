import tommorow_data_get
import torch
import pandas as pd
from elec_prediction import convert_elec
from solar_prediction import convert_solar
from dataset_define import ElecDemandDataset, SunlightDataset, Windpower_Dataset
from torch.utils.data import DataLoader

data_origin = tommorow_data_get.get_data()

elec_model_path = 'models/elec_model.pt'
solar_model_path = 'models/solar_model.pt'
wind_model_path = 'models/wind_model.pt'

elec_model = torch.load(elec_model_path, map_location=torch.device('cpu'))
solar_model = torch.load(solar_model_path, map_location=torch.device('cpu'))
#wind_model = torch.load(wind_model_path, map_location=torch.device('cpu'))

features_test_elec = convert_elec(data_origin)
labels_test_elec = pd.DataFrame({'label': [0] * len(features_test_elec)})
test_dataset_elec = ElecDemandDataset(features_test_elec, labels_test_elec)
test_loader_elec = DataLoader(test_dataset_elec, batch_size=1, shuffle=False)

features_test_solar = convert_solar(data_origin)
labels_test_solar = pd.DataFrame({'label': [0] * len(features_test_solar)})
test_dataset_solar = SunlightDataset(features_test_solar, labels_test_solar)
test_loader_solar = DataLoader(test_dataset_solar, batch_size=1, shuffle=False)

features_test_wind = convert_wind(data_origin)
labels_test_wind = pd.DataFrame({'label': [0] * len(features_test_wind)})
test_dataset_wind = Windpower_Dataset(features_test_wind, labels_test_wind)
test_loader_wind = DataLoader(test_dataset_wind, batch_size=1, shuffle=False)

# GPU를 사용할 경우
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 전력 데이터에 대한 예측
y_pred_elec = []
elec_model.eval()
with torch.no_grad():
    for i, (features, labels) in enumerate(test_loader_elec):
        features = features.to(device)
        labels = labels.to(device)

        outputs = elec_model(features).squeeze(-1)
        outputs[outputs < 3] = 0

        for seq_idx in range(outputs.shape[-1]):
            y_pred_elec.append(outputs[:, seq_idx].item())

# 태양광 데이터에 대한 예측
y_pred_solar = []
solar_model.eval()
with torch.no_grad():
    for i, (features, labels) in enumerate(test_loader_solar):
        features = features.to(device)
        labels = labels.to(device)

        outputs = solar_model(features).squeeze(-1)
        outputs[outputs < 3] = 0

        for seq_idx in range(outputs.shape[-1]):
            y_pred_solar.append(outputs[:, seq_idx].item())

# 풍력 데이터에 대한 예측
y_pred_wind = []
wind_model.eval()
with torch.no_grad():
    for i, (features, labels) in enumerate(test_loader_wind):
        features = features.to(device)
        labels = labels.to(device)

        outputs = wind_model(features).squeeze(-1)
        outputs[outputs < 3] = 0

        for seq_idx in range(outputs.shape[-1]):
            y_pred_wind.append(outputs[:, seq_idx].item())

print(y_pred_elec)
print(y_pred_solar)
print(y_pred_wind)