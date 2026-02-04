import { Eye } from "lucide-react";
import Checkbox from "./Checkbox";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function SignupForm() {
  const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name,setName]=useState("")
    const [error ,setError]=useState("")
    const [show,setShow]=useState(true)
    const handleSubmit = async (e) => {
      e.preventDefault(); 
    if(!email){
      setError("enter the email")
      return
    }else if(!password){
      setError("enter the password")
      return
    }else if(!name){
      setError("enter the name")
      return
    }
  const res = await fetch("http://localhost:5000/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password })
  });

  const data = await res.json();
  alert(`${data.msgs}signup successfully`);
  navigate("/");
};
  function toogleaction(){
    setShow(!show)
  }
  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-sm text-white">
      {/* Email */}
      <div>
        <label className="text-xs text-gray-400">EMAIL ADDRESS</label>
        <input
          type="email"
          placeholder="hello@reallygreatsite.com"
          className="w-full bg-transparent border-b border-gray-600 focus:border-yellow-400 outline-none py-1 text-sm"
          onChange={(e)=>setEmail(e.target.value)}
        />
      </div>

      {/* Full Name */}
      <div>
        <label className="text-xs text-gray-400">FULL NAME</label>
        <input
          type="text"
          placeholder="Samira Hadid"
          className="w-full bg-transparent border-b border-gray-600 focus:border-yellow-400 outline-none py-1 text-sm"
          onChange={(e)=>setName(e.target.value)}
        />
      </div>

      {/* Password */}
      <div className="relative">
        <label className="text-xs text-gray-400">PASSWORD</label>
        <input
          type="password"
          placeholder="********"
          className="w-full bg-transparent border-b border-gray-600 focus:border-yellow-400 outline-none py-1 text-sm pr-6"
          onChange={(e)=>setPassword(e.target.value)}
        />
        <Eye onClick = {toogleaction}size={16} className="absolute right-0 bottom-1 text-gray-400 cursor pointer" />
      </div>
      {error &&(
        <p className="text-red-500 mt-2">
          {error}
        </p>
      )}

      <Checkbox />

      {/* Buttons */}
      <div className="flex gap-3 mt-4">
        <button
          type="submit"
          className="flex-1 bg-gradient-to-r from-sky-500 to-blue-700 text-white rounded-full py-2 font-medium hover:opacity-90"
        >
          Enter
        </button>
        <button
          type="button"
          className="flex-1 border border-sky-500 text-sky-400 rounded-full py-2 font-medium hover:bg-sky-950/30"
          onClick={()=>navigate("/login")}
        >
          Login
        </button>
      </div>
    </form>
  );
}
