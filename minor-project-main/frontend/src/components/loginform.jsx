import { Eye } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
export default function LoginForm() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError]= useState("")
    const handleSubmit = async (e) => {
      e.preventDefault(); 
      if(!email){
        setError("Please enter the email")
        return
      }
      else if(!password){
        setError("Please enter the password")
        return 
      }
      else{
        setError("")
      }
    
    const res = await fetch("http://localhost:5000/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();
  alert(`${data.msg}loged in successfully`);

  navigate("/");
};
  return (
    <form onSubmit={handleSubmit}className="flex flex-col gap-4 w-full max-w-sm text-white">
      {/* Email */}
      <div>
        <label className="text-xs text-gray-400">EMAIL ADDRESS</label>
        <input
          value={email}
          type="email"
          placeholder="hello@reallygreatsite.com"
          className="w-full bg-transparent border-b border-gray-600 focus:border-yellow-400 outline-none py-1 text-sm"
          onChange={(e)=>setEmail(e.target.value)}
        />
      </div>

      

      {/* Password */}
      <div className="relative">
        <label className="text-xs text-gray-400">PASSWORD</label>
        <input
          value={password}
          type="password"
          placeholder="********"
          className="w-full bg-transparent border-b border-gray-600 focus:border-yellow-400 outline-none py-1 text-sm pr-6"
          onChange={(e) => setPassword(e.target.value)}
        />
        <Eye size={16} className="absolute right-0 bottom-1 text-gray-400" />
      </div>
      
      {error && (
        <p className="text-red-500 mt-2">
          {error}
        </p>
      )}

      

      {/* Buttons */}
      <div className="flex gap-3 mt-4">
        <button
          type="submit"
          className="flex-1 bg-gradient-to-r from-sky-500 to-blue-700 text-white rounded-full py-2 font-medium hover:opacity-90"
        >
          Enter
        </button>
      </div>
    </form>
  );
}
