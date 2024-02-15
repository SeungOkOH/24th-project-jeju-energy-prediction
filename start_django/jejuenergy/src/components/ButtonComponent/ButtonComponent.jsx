import "./ButtonComponent.css";
import { GoSun } from "react-icons/go";
import { LuWind } from "react-icons/lu";
import { LiaTemperatureHighSolid } from "react-icons/lia";
import { IoNewspaperOutline } from "react-icons/io5";




function ButtonComponent() {
  return (
    <div className="button-div">
      <p className="button-p">MAIN CONTENTS</p>
      <div className="buttons">
        <button className="button-">
          <GoSun size="24" color="FEBB50" />
          <div className="button-detail">
            <p className="button-p1">TOMORROW FORECAST</p>
            <p className="button-p2">
              SOLAR POWER
              <br />
              (download csv file)
            </p>
          </div>
        </button>
        <button className="button-">
          <LuWind size="24" color="2D77E7" />
          <div className="button-detail">
            <p className="button-p1">TOMORROW FORECAST</p>
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
        <button className="button-">
          <IoNewspaperOutline size="24" color="616161" />
          <div className="button-detail">
            <p className="button-p1">MANAGEMENT</p>
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
