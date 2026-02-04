import background from "../assets/background.png"
import { Lock, UserPlus, Shield, Zap } from "lucide-react";
import React from "react";
import { useNavigate } from "react-router-dom";

const Hero = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-wrap items-center justify-center lg:justify-between px-6 lg:px-16 py-20 bg-[#0d0d1a] text-white">

      {/* Left Image */}
      <div className="w-full lg:w-1/2 flex justify-center mb-10 lg:mb-0">
        <img
          src={background}
          alt="photo"
          className="w-64 sm:w-72 md:w-96 lg:w-[450px]"
        />
      </div>

      {/* Right Content */}
      <div className="w-full lg:w-1/2 bg-gradient-to-b from-[#0c0f1e] to-[#0d1228] text-white flex flex-col items-center py-12 px-4 rounded-xl">

        {/* Main Heading */}
        <h1 className="text-4xl sm:text-5xl font-extrabold text-center">
          AUTO_INSIGHT
        </h1>

        <h2 className="text-xl sm:text-3xl font-bold text-blue-400 mt-3 text-center">
          Smarter Login. Smarter Insights.
        </h2>

        {/* Subtext */}
        <p className="text-gray-300 text-center max-w-xl mt-4 text-base sm:text-lg">
          Securely log in or create your account to explore data automation,
          instant analysis, and personalized insights powered by machine learning.
        </p>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-14 max-w-5xl w-full">

          {/* Instant Access */}
          <div className="bg-[#10172d] border border-gray-700 rounded-2xl p-6 text-center hover:border-blue-500 transition">
            <Zap className="mx-auto text-blue-400" size={35} />
            <h3 className="text-lg font-semibold mt-4">Instant Access</h3>
            <p className="text-gray-400 mt-2 text-sm">
              Login to get immediate access to your dashboard and tools.
            </p>
          </div>

          {/* Create Account */}
          <div className="bg-[#10172d] border border-gray-700 rounded-2xl p-6 text-center hover:border-blue-500 transition">
            <UserPlus className="mx-auto text-green-400" size={35} />
            <h3 className="text-lg font-semibold mt-4">Easy Signup</h3>
            <p className="text-gray-400 mt-2 text-sm">
              Create an account in seconds and start analyzing instantly.
            </p>
          </div>

          {/* Privacy */}
          <div className="bg-[#10172d] border border-gray-700 rounded-2xl p-6 text-center hover:border-blue-500 transition">
            <Shield className="mx-auto text-yellow-400" size={35} />
            <h3 className="text-lg font-semibold mt-4">Privacy First</h3>
            <p className="text-gray-400 mt-2 text-sm">
              We protect your data using secure authentication systems.
            </p>
          </div>

        </div>

        {/* Button */}
        <button
          onClick={() => navigate("/upload")}
          className="mt-12 bg-blue-600 hover:bg-blue-700 px-10 py-4 text-lg font-semibold rounded-full shadow-lg transition"
        >
          Get started
        </button>

        <p className="mt-3 text-gray-500 text-sm">
          No complicated setup · Secure Authentication · Fast Access
        </p>
      </div>
    </div>
  );
};

export default Hero;
