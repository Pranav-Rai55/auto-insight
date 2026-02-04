import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Menu, X } from "lucide-react";

export default function Navbar() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  return (
    <nav className="bg-black text-white px-6 py-4 border-b border-yellow-400">
      
      {/* NAVBAR CONTAINER */}
      <div className="flex justify-between items-center">

        {/* LOGO */}
        <h1 className="text-yellow-400 text-2xl font-bold tracking-wide">
          AUTO INSIGHT
        </h1>

        {/* MOBILE MENU BUTTON */}
        <button
          className="lg:hidden block text-yellow-400"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={28} /> : <Menu size={28} />}
        </button>

        {/* DESKTOP MENU */}
        <div className="hidden lg:flex items-center gap-10">
          <ul className="flex gap-8 text-lg font-medium">
            <li className="text-yellow-500 cursor-pointer">Home</li>
            <li className="text-yellow-500 cursor-pointer">About Us</li>
            <li className="text-yellow-500 cursor-pointer">Contact Us</li>
          </ul>

          <div className="flex gap-3">
            <button
              onClick={() => navigate("/login")}
              className="bg-yellow-400 text-black px-4 py-2 rounded-lg font-semibold hover:bg-yellow-300"
            >
              Login
            </button>

            <button
              onClick={() => navigate("/signup")}
              className="bg-yellow-400 text-black px-4 py-2 rounded-lg font-semibold hover:bg-yellow-300"
            >
              Signup
            </button>
          </div>
        </div>
      </div>

      {/* MOBILE DROPDOWN MENU */}
      {open && (
        <div className="lg:hidden mt-4 animate-fadeIn">
          <ul className="flex flex-col gap-4 text-lg font-medium">
            <li className="text-yellow-500 cursor-pointer">Home</li>
            <li className="text-yellow-500 cursor-pointer">About Us</li>
            <li className="text-yellow-500 cursor-pointer">Contact Us</li>
          </ul>

          <div className="flex flex-col gap-3 mt-4">
            <button
              onClick={() => navigate("/login")}
              className="bg-yellow-400 text-black px-4 py-2 rounded-lg font-semibold hover:bg-yellow-300"
            >
              Login
            </button>

            <button
              onClick={() => navigate("/signup")}
              className="bg-yellow-400 text-black px-4 py-2 rounded-lg font-semibold hover:bg-yellow-300"
            >
              Signup
            </button>
          </div>
        </div>
      )}
    </nav>
  );
}
