import LoginForm from "./loginform";
import mainbg from "../assets/mainbg.jpeg"
import loginimage from"../assets/loginimage.png"

export default function LoginCard() {
   

  return (
      <div
      className="flex items-center justify-center h-screen bg-cover bg-center brightness-100 bg-gradient-to-br from-[#1b1202] to-[#2c2105]"
      style={{ backgroundImage: `url(${mainbg})` }}
    >
      <div className="bg-gradient-to-br from-[#1b1202] to-[#2c2105] rounded-2xl p-10 flex items-center shadow-lg shadow-black/60 border border-[#3a2a0a] w-[700px] text-white border-white">
      
        {/* Left: Form */}
        <div className="flex-1">
          <LoginForm />
        </div>

        {/* Right: Image + Title */}
        <div className="flex flex-col items-center justify-center flex-1">
          <h2 className="text-2xl font-semibold mb-4 text-white">Login</h2>
          
          <div className="flex items-center justify-center">
            <img src={loginimage} alt="photo" className="w-auto h-auto max-w-[200px]"></img>
          </div>
          
        </div>
      </div>
    </div>
  );
}
