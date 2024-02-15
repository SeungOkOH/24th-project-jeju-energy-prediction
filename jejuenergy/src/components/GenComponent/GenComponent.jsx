import "./GenComponent.css";
import axios from "axios";
import { useState, useEffect } from "react";

function GenComponent() {
  const [solarGraph, setSolarGraph] = useState("/solar_output.png");
  const [windGraph, setWindGraph] = useState("/solar_output.png");
  const [loading, setLoading] = useState(true);

  //backend에서 데이터 받아오기 (그래프 시각화하나 url을 보내줘야함 Django)
  useEffect(() => {
    const fetchGraphData = async () => {
      try {
        const solarResponse = await axios.get("/solar_graph_url");
        const windResponse = await axios.get("/wind_graph_url");
        setSolarGraph(solarResponse.data.image_url);
        setWindGraph(windResponse.data.image_url);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching graph data:", error);
      }
    };

    fetchGraphData();
  }, []);

  return (
    <div className="gen-div">
      <div className="gen-welcome">
        <p className="p-welcome">WELCOME TO JEJU!</p>
      </div>
      <div className="gen-graph">
        <img className="gen-img" src={solarGraph} alt="Solar Graph" />
      </div>
      <div className="gen-graph">
        <img className="gen-img" src={windGraph} alt="Wind Graph" />
      </div>
    </div>
  );
}

export default GenComponent;
