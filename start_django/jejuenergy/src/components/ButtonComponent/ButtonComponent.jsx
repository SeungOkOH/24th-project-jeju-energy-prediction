import "./ButtonComponent.css";
import { GoSun } from "react-icons/go";
import { LuWind } from "react-icons/lu";
import { LiaTemperatureHighSolid } from "react-icons/lia";
import { IoNewspaperOutline } from "react-icons/io5";
import React, { useState, useEffect } from "react";

import axios from "axios";



function ButtonComponent() {
  
  const [loading, setLoading] = useState(true);
  const [solarCSV, setsolarCSV] = useState(null);
  const [windCSV, setwindCSV] = useState(null);
  
  const handlesolarBtnClick = () => {
    const link = document.createElement('a');
    link.href = solarCSV;
    link.setAttribute('download', 'solar_prediction.csv');
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  };

  const handlewindBtnClick = () => {
    const link = document.createElement('a');
    link.href = windCSV;
    link.setAttribute('download', 'wind_prediction.csv');
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response_solar = await axios.get('/solar_csv/', {
          responseType: "blob",
        });
        const response_wind = await axios.get('/wind_csv/', {
          responseType: "blob",
        });

        setsolarCSV(URL.createObjectURL(response_solar.data));
        setwindCSV(URL.createObjectURL(response_wind.data));

        setLoading(false);
      }
      catch (error) {
        console.log("Error fetching data: ", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="button-div">
      <p className="button-p">MAIN CONTENTS</p>
      <div className="buttons">
        <button className="button-" onClick = {() => handlesolarBtnClick('')} disabled = {loading}>
          <GoSun size="24" color="FEBB50" />
          <div className="button-detail">
            <p className="button-p1">TOMORROW FORECAST {!loading || "(Preparing...)"}</p>
            <p className="button-p2">
              SOLAR POWER
              <br />
              (download csv file)
            </p>
          </div>
        </button>
        <button className="button-" onClick = {() => handlewindBtnClick()} disabled = {loading}>
          <LuWind size="24" color="2D77E7" />
          <div className="button-detail">
            <p className="button-p1">TOMORROW FORECAST {!loading || "(Preparing...)"}</p>
            <p className="button-p2">
              WIND POWER
              <br />
              (download csv file)
            </p>
          </div>
        </button>
        <button
          onClick={() =>
            window.open("https://www.kma.go.kr/jeju/html/main/index.jsp")
          }
          className="button-"
        >
          <LiaTemperatureHighSolid size="24" color="FF7E86" />
          <div className="button-detail">
            <p className="button-p1">WEATHER INFO</p>
            <p className="button-p2">
              TODAY'S WEATHER INFO
              <br />
              (go to the website)
            </p>
          </div>
        </button>
        <button className="button-" disabled = {loading}>
          <IoNewspaperOutline size="24" color="616161" />
          <div className="button-detail">
            <p className="button-p1">MANAGEMENT {!loading || "(Preparing...)"}</p>
            <p className="button-p2">
              DEMAND FORECAST
              <br />& GREENGEN ANALYZER
            </p>
          </div>
        </button>
      </div>
    </div>
  );
}

export default ButtonComponent;
