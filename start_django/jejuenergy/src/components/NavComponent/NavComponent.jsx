import "./NavComponent.css";

function NavComponent() {
  return (
    <div className="nav-div">
      <nav>
        <div className="nav-bar"></div>
        <ul className="nav-ul">
          <li className="nav-li">
            <a href="#home" className="nav-a">
              Home
            </a>
          </li>
          <li className="nav-li">
            <a href="#about" className="nav-a">
              About Us
            </a>
          </li>
          <li>JEJU ENERGY INNOVATOR</li>
          <li className="nav-li">
            <a href="#services" className="nav-a">
              Services
            </a>
          </li>
          <li className="nav-li">
            <a href="#contact" className="nav-a">
              Contact
            </a>
          </li>
        </ul>
      </nav>
    </div>
  );
}
export default NavComponent;
