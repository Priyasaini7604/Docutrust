import { useDropzone } from "react-dropzone";
import { FileText, CheckCircle, Upload } from "lucide-react";

function PDFUploader({ uploadedFile, setUploadedFile }) {
  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file && file.type === "application/pdf") {
      setUploadedFile(file);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    multiple: false,
  });

  return (
    <div className="uploader-container">
      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? "dropzone-active" : ""} 
                    ${uploadedFile ? "dropzone-success" : ""}`}
      >
        <input {...getInputProps()} />

        {uploadedFile ? (
          // File uploaded state
          <div className="upload-success">
            <CheckCircle size={40} color="#22c55e" />
            <p className="upload-filename">{uploadedFile.name}</p>
            <p className="upload-hint">Click to replace file</p>
          </div>
        ) : (
          // Empty state
          <div className="upload-empty">
            <Upload size={40} color="#4f8ef7" />
            <p className="upload-title">Drop PDF here</p>
            <p className="upload-hint">or click to browse</p>
          </div>
        )}
      </div>

      {/* File Info */}
      {uploadedFile && (
        <div className="file-info">
          <div className="file-info-row">
            <FileText size={16} color="#4f8ef7" />
            <span className="file-info-name">{uploadedFile.name}</span>
          </div>
          <div className="file-info-row">
            <span className="file-info-label">Size:</span>
            <span className="file-info-value">
              {(uploadedFile.size / 1024).toFixed(1)} KB
            </span>
          </div>
          <div className="file-info-row">
            <span className="file-info-label">Status:</span>
            <span className="file-info-status">Ready to process ✅</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default PDFUploader;