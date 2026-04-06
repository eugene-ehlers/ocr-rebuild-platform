import { Link } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function PreUploadPage() {
  return (
    <PageScaffold
      title="Upload your document"
      summary="Drag and drop or select a file to proceed."
    >
      <div className="upload-zone">
        <p><strong>Drag & drop your file here</strong></p>
        <p>or</p>
        <button className="btn">Choose file</button>
        <p>PDF, JPG, PNG — Max 10MB</p>
      </div>

      <Link to="/submit" className="btn">
        Continue to review
      </Link>
    </PageScaffold>
  );
}
