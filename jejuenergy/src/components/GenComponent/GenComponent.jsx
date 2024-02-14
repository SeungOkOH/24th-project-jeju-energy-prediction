import "./GenComponent.css";

function GenComponent() {
  return (
    <div className="gen-div">
      <div className="gen-welcome">
        <p className="p-welcome">WELCOME TO JEJU!</p>
      </div>
      <div className="gen-graph">
        <img
          className="gen-img"
          src="/solar_output.png"
          alt="로드에 실패했습니다."
        />
      </div>
      <div className="gen-graph">
        <img
          className="gen-img"
          src="/solar_output.png"
          alt="로드에 실패했습니다."
        />
      </div>
    </div>
  );
}

export default GenComponent;
