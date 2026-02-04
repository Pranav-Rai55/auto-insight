import FileUpload from "../components/fileupload";
import background from "../assets/background.png";
import Navbar from "../components/navbar";
import Footer from "../components/Footer";

export default function Hero() {
  return (
    <div className="bg-[#0d0d1a] text-white min-h-screen flex flex-col">

      {/* MAIN CONTENT */}
      <div className="
        flex flex-col-reverse lg:flex-row 
        items-center justify-between 
        px-6 lg:px-16 
        py-10 lg:py-20 
        flex-grow
      ">

        {/* LEFT IMAGE */}
        <div className="w-full lg:w-1/2 flex justify-center mt-10 lg:mt-0">
          <img
            src={background}
            alt="photo"
            className="w-64 sm:w-80 md:w-96 lg:w-[450px]"
          />
        </div>

        {/* RIGHT DRAG & DROP BOX */}
        <div className="w-full lg:w-1/2 flex flex-col items-center justify-center">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-amber-600 mb-6 text-center">
            Upload Your File
          </h1>

          <div className="w-full max-w-xl">
            <FileUpload />
          </div>
        </div>
      </div>

    </div>
  );
}
