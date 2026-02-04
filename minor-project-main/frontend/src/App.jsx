import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar"
import Home from "./pages/Hero"
import Footer from "./components/Footer"
import LoginCard from "./components/logincard";
import SignupCard from "./components/SignupCard";
import Hero2 from "./pages/Hero2";

 function App() {
  return(
  <>
    
     <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="login" element={<LoginCard />} />
        <Route path="signup" element={<SignupCard />} />
        <Route path="upload" element={<Hero2/>} />
      </Routes>
      <Footer />
    
  </>
  
  
  );
  
}
export default App
