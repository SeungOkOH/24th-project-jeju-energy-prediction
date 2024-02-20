import React, { useEffect, useState } from "react";
import axios from "axios";

import "./DemandComponent.css";
import { MdAccessAlarm } from "react-icons/md";
import { MdOutlineLocalFireDepartment } from "react-icons/md";

function getTomorrowDate() {
  const today = new Date(); // 현재 날짜와 시간
  const tomorrow = new Date(today); // today 객체 복사
  tomorrow.setDate(tomorrow.getDate() + 1); // 내일 날짜 설정

  // 날짜 포맷팅: YYYY-MM-DD
  const yyyy = tomorrow.getFullYear();
  const mm = String(tomorrow.getMonth() + 1).padStart(2, "0"); // 월은 0부터 시작하므로 1을 더해줍니다.
  const dd = String(tomorrow.getDate()).padStart(2, "0");

  return `${yyyy}/${mm}/${dd}`;
}
const removeDecimal = (str) => {
  return str.replace(/\.\d+$/, "");
};

function DemandComponent() {
  const [solarGen, setSolarGen] = useState("Loading");
  const [windGen, setWindGen] = useState("Loading");
  const [demandPredictions, setDemandPredictions] = useState("Loading");
  const [dataSets, setDataSets] = useState([]);
  const [dataSets1, setDataSets1] = useState([]);
  const [demandGraph, setDemandGraph] = useState("");
  const [loading, setLoading] = useState("");
  const [tomorrowDate, setTomorrowDate] = useState("");

  // 이미지 클릭 핸들러 함수
  const handleImageClick = (imageUrl) => {
    window.open(imageUrl, "_blank");
  };

  useEffect(() => {
    const date = getTomorrowDate();
    setTomorrowDate(date);
  }, []);
  // backend에서 데이터 받아오기
  // 조건 : solar + wind가 demand보다 크면
  // {time, demand, solarGen, windGen} 형태로 보내야함.

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/alert_data/");
        //화석연료쪽
        const newDataSets = response.data.map((item) => ({
          time: `${item.index}:00`,
          demand: item.elec,
          solarGen: item.solar,
          windGen: item.wind,
        }));
        setDataSets1(newDataSets);
        console.log(newDataSets);
        //내림차순 전력
        if (response.data && response.data.length > 0) {
          const sortedData = response.data.sort((a, b) => {
            const totalGenA = parseFloat(a.solar) + parseFloat(a.wind);
            const totalGenB = parseFloat(b.solar) + parseFloat(b.wind);
            return totalGenB - totalGenA;
          });

          const newDataSets = sortedData.map((item) => ({
            time: `${item.index}:00`,
            demand: parseFloat(item.elec),
            solarGen: parseFloat(item.solar),
            windGen: parseFloat(item.wind),
            totalRenewableGen: parseFloat(item.solar) + parseFloat(item.wind),
          }));

          setDataSets(newDataSets);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  // demand graph 받아오기
  useEffect(() => {
    const fetchGraphData = async () => {
      setLoading(true);
      try {
        // Blob 형태로 이미지 데이터를 받아옵니다.
        const demandResponse = await axios.get("/demand_graph/", {
          responseType: "blob",
        });

        // Blob 데이터를 객체 URL로 변환합니다.
        setDemandGraph(URL.createObjectURL(demandResponse.data));
      } catch (error) {
        console.error("Error fetching graph data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchGraphData();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="demand-div">
      <div className="demand-wrapper">
        <img
          className="demand-img"
          src={demandGraph}
          alt="Demand Graph"
          onClick={() => handleImageClick(demandGraph)}
        />
      </div>

      <div className="alert-div">
        <h1>
          RENEWABLE ENERGY GEN IN DESCENDING ORDER
          <MdAccessAlarm size="24" color="CC6D6D" />
        </h1>
        {/* 시간대 세트로 보여주기 */}
        <h2 className="fortomorrow">for tomorrow ({tomorrowDate})</h2>
        {dataSets.map((item) => (
          <div key={item.time} className="data-set">
            <h3>{item.time}</h3>
            <h4>
              DEMAND <br /> {Math.floor(Number(item.demand))}
            </h4>
            <h4>
              SOLAR <br /> {Math.floor(Number(item.solarGen))}
            </h4>
            <h4>
              WIND <br /> {Math.floor(Number(item.windGen))}
            </h4>
            <h5 className="surplus">
              TOTAL
              <br />
              <p className="greengen">GREENGEN</p>
              <p className="totalgen">
                {Math.floor(Number(item.totalRenewableGen))}
              </p>
            </h5>
          </div>
        ))}
      </div>
      <div className="alert-div">
        <h1>
          FOSSIL FUEL GEN PROPOSAL
          <MdOutlineLocalFireDepartment size="24" color="C8A190" />
        </h1>
        <h2 className="fortomorrow">for tomorrow ({tomorrowDate})</h2>
        {dataSets1.map((item) => {
          if (item.demand > item.solarGen + item.windGen) {
            return (
              <div key={item.time} className="data-set">
                <h3>{item.time}</h3>
                <h4>
                  DEMAND <br /> {Math.floor(Number(item.demand))}
                </h4>
                <h4>
                  SOLAR <br /> {Math.floor(Number(item.solarGen))}
                </h4>
                <h4>
                  WIND <br /> {Math.floor(Number(item.windGen))}
                </h4>
                <h5 className="proposal">
                  PROPOSAL <br />{" "}
                  {Math.floor(
                    Number(item.demand - item.solarGen - item.windGen)
                  )}
                </h5>
              </div>
            );
          }
          return null;
        })}
      </div>
    </div>
  );
}

export default DemandComponent;
