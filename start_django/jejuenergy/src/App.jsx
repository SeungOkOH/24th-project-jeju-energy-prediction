
import './App.css';
import DemandComponent from './components/DemandComponent/DemandComponent';
import ButtonComponent from './components/ButtonComponent/ButtonComponent';
import GenComponent from './components/GenComponent/GenComponent';
import NavComponent from './components/NavComponent/NavComponent';

function App() {
  return (
    <div className="App">
     <NavComponent/>
     <GenComponent/>
     <ButtonComponent/>
     <DemandComponent/>
    </div>
  );
}

export default App;
