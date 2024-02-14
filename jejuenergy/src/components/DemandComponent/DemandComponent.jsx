import React, { useEffect, useState } from "react";
import axios from "axios";

import "./DemandComponent.css";
import { MdAccessAlarm } from "react-icons/md";
import { MdOutlineLocalFireDepartment } from "react-icons/md";

function DemandComponent() {
  const [solarGen, setSolarGen] = useState("Loading");
  const [windGen, setWindGen] = useState("Loading");
  const [demandPredictions, setDemandPredictions] = useState("Loading");
  const [dataSets, setDataSets] = useState([
    { time: "14:20 pm", demand: 100, solarGen: 130, windGen: 150 },
  ]);

  // backend에서 데이터 받아오기
  // 조건 : solar + wind가 demand보다 크면
  // {time, demand, solarGen, windGen} 형태로 보내야함.

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("/api/demand-data");
        const newDataSets = response.data.map((item) => ({
          time: item.time,
          demand: item.demand,
          solarGen: item.solarGen,
          windGen: item.windGen,
        }));
        setDataSets(newDataSets);
      } catch (error) {
        // Handle error
      }
    };

    fetchData();
  }, []);

  return (
    <div className="demand-div">
      <div className="demand-wrapper">
        <img
          className="demand-img"
          src="/solar_output.png"
          alt="로드에 실패했습니다."
        />
      </div>

      <div className="alert-div">
        <h1>
          GREENGEN SURPLUS ALERT
          <MdAccessAlarm size="24" color="CC6D6D" />
        </h1>
        {/* 시간대 세트로 보여주기 */}

        {dataSets.map((item) => (
          <div key={item.time} className="data-set">
            <h3>{item.time}</h3>
            <h4>
              DEMAND <br /> {item.demand}
            </h4>
            <h4>
              SOLAR <br /> {item.solarGen}
            </h4>
            <h4>
              WIND <br /> {item.windGen}
            </h4>
            <h5 className="surplus">
              SURPLUS <br /> {item.windGen + item.solarGen - item.demand}
            </h5>
          </div>
        ))}
      </div>
      <div className="alert-div">
        <h1>
          FOSSIL FUEL GEN PROPOSAL
          <MdOutlineLocalFireDepartment size="24" color="C8A190" />
        </h1>
      </div>
    </div>
  );
}

export default DemandComponent;
