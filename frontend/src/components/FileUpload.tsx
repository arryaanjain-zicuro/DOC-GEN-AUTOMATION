import React, { useState } from 'react';

const FileUpload = () => {
  const [docxFile, setDocxFile] = useState<File | null>(null);
  const [xlsxFile, setXlsxFile] = useState<File | null>(null);

  const handleDocxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setDocxFile(event.target.files[0]);
    }
  };

  const handleXlsxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setXlsxFile(event.target.files[0]);
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // Handle file upload logic here
    console.log('DOCX File:', docxFile);
    console.log('XLSX File:', xlsxFile);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-100 to-indigo-200">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center text-indigo-700">Upload Your Documents</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload <span className="font-semibold text-indigo-600">Alpha DOCX</span> file:
            </label>
            <input
              type="file"
              accept=".docx"
              onChange={handleDocxChange}
              className="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
            />
            {docxFile && (
              <p className="mt-2 text-xs text-green-600">Selected: {docxFile.name}</p>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload <span className="font-semibold text-indigo-600">Beta XLSX</span> file:
            </label>
            <input
              type="file"
              accept=".xlsx"
              onChange={handleXlsxChange}
              className="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
            />
            {xlsxFile && (
              <p className="mt-2 text-xs text-green-600">Selected: {xlsxFile.name}</p>
            )}
          </div>
          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 rounded-md font-semibold hover:bg-indigo-700 transition"
          >
            Upload
          </button>
        </form>
      </div>
    </div>
  );
};

export default FileUpload;