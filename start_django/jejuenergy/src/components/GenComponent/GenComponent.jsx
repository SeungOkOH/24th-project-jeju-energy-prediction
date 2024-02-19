import "./GenComponent.css";
import axios from "axios";
import { useState, useEffect } from "react";

function GenComponent() {
  const [solarGraph, setSolarGraph] = useState(null);
  const [windGraph, setWindGraph] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGraphData = async () => {
      setLoading(true);
      try {
        // Blob 형태로 이미지 데이터를 받아옵니다.
        const solarResponse = await axios.get("/solar_graph/", {
          responseType: "blob",
        });
        const windResponse = await axios.get("/wind_graph/", {
          responseType: "blob",
        });

        // Blob 데이터를 객체 URL로 변환합니다.
        setSolarGraph(URL.createObjectURL(solarResponse.data));
        setWindGraph(URL.createObjectURL(windResponse.data));
      } catch (error) {
        console.error("Error fetching graph data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchGraphData();
  }, []);

  if (loading) return <div>Loading...</div>;

  // 이미지 클릭 핸들러 함수
  const handleImageClick = (imageUrl) => {
    window.open(imageUrl, "_blank");
  };

  return (
    <div className="gen-div">
      <div className="gen-welcome">
        <p className="p-welcome">WELCOME TO JEJU!</p>
      </div>
      <div className="gen-graph">
        {solarGraph && (
          <img
            className="gen-img"
            src={solarGraph}
            alt="Solar Graph"
            onClick={() => handleImageClick(solarGraph)} // 이미지 클릭 이벤트
          />
        )}
      </div>
      <div className="gen-graph">
        {windGraph && (
          <img
            className="gen-img"
            src={windGraph}
            alt="Wind Graph"
            onClick={() => handleImageClick(windGraph)} // 이미지 클릭 이벤트
          />
        )}
      </div>
    </div>
  );
}

export default GenComponent;
