import React, { useState } from "react";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleDragOver = (e) => e.preventDefault();

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    setFile(droppedFile);
    uploadFile(droppedFile);
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    uploadFile(selectedFile);
  };

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/process", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      console.log("Processed Data:", data);
      setResponse(data);   //  store response
      if (data.html_url) {
      window.location.href = data.html_url;
    }
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <div className="flex flex-col items-center mt-12">
      <label
        htmlFor="fileInput"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className="
          w-9/10 h-32 sm:h-40
          flex flex-col justify-center items-center gap-3
          bg-white/5 backdrop-blur-xl
          border-2 border-dashed border-gray-500
          rounded-2xl
          shadow-lg shadow-blue-500/10
          cursor-pointer
          transition-all duration-300
          hover:border-blue-400 hover:bg-white/10 hover:scale-[1.02]
        "
      >
        <div className="flex flex-col items-center">
          <svg
            className="w-12 h-12 text-blue-400"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3 15v4a2 2 0 002 2h14a2 2 0 002-2v-4M7 10l5-5m0 0l5 5m-5-5v12"
            />
          </svg>

          <p className="text-gray-300 font-medium text-lg">
            Drag & Drop your file here
          </p>
          <p className="text-gray-400 text-sm">or click to upload</p>
        </div>

        <input
          id="fileInput"
          type="file"
          onChange={handleFileSelect}
          className="hidden"
        />
      </label>

      {file && (
        <p className="mt-5 text-blue-400 font-semibold text-lg">
          Selected: <span className="text-white">{file.name}</span>
        </p>
      )}

      {/* ✔ Show Backend Response */}
      {response && (
        <div className="mt-6 text-white text-lg bg-white/10 p-4 rounded-xl shadow-md">
          <p>📌 <strong>Rows:</strong> {response.rows}</p>
          <p>📁 <strong>Columns:</strong> {response.columns.join(", ")}</p>
        </div>
      )}
      {file && (
    <button
        onClick={() => uploadFile(file)}
        className="mt-4 px-6 py-2 bg-amber-600 text-white rounded-lg shadow-md hover:bg-blue-700"
    >
      Process File
    </button>
    )}
    </div>
  );
}
