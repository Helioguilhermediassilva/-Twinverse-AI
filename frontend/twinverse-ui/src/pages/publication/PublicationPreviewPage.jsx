import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import PublicationViewer from '../components/publication/PublicationViewer';
import SharingButtons from '../components/publication/SharingButtons';
import LoadingIndicator from '../components/LoadingIndicator';
import ErrorMessage from '../components/ErrorMessage';
import { getPublicationStatus } from '../services/publicationService';

const PublicationPreviewPage = () => {
  const { publicationId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [publicationData, setPublicationData] = useState(null);
  
  useEffect(() => {
    const fetchPublicationData = async () => {
      try {
        const data = await getPublicationStatus(publicationId);
        setPublicationData(data);
        setLoading(false);
      } catch (err) {
        setError(err.message || 'Error loading publication');
        setLoading(false);
      }
    };
    
    fetchPublicationData();
  }, [publicationId]);
  
  const handleStartOver = () => {
    // Navigate back to home page to start a new creation
    navigate('/');
  };
  
  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-center">Your Twinverse Experience</h1>
        
        {error && <ErrorMessage message={error} />}
        
        {loading ? (
          <div className="text-center">
            <LoadingIndicator />
            <p className="mt-4">Loading your publication...</p>
          </div>
        ) : (
          <>
            {publicationData && publicationData.status === 'completed' ? (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="mb-6">
                  <h2 className="text-xl font-semibold mb-4 text-center">Publication Preview</h2>
                  
                  <div className="mb-6 p-4 bg-gray-50 rounded-md">
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-sm font-medium text-gray-500">Public URL:</span>
                      <a 
                        href={publicationData.public_url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline break-all"
                      >
                        {publicationData.public_url}
                      </a>
                    </div>
                    <div className="flex justify-end">
                      <button 
                        onClick={() => navigator.clipboard.writeText(publicationData.public_url)}
                        className="text-sm bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded"
                      >
                        Copy URL
                      </button>
                    </div>
                  </div>
                  
                  <PublicationViewer htmlUrl={publicationData.html_url} />
                  
                  <div className="mt-8">
                    <h3 className="text-lg font-medium mb-3">Share Your Experience</h3>
                    <SharingButtons publicUrl={publicationData.public_url} />
                  </div>
                </div>
                
                <div className="flex justify-center mt-8">
                  <button 
                    onClick={handleStartOver}
                    className="btn-primary text-lg px-8 py-3"
                  >
                    Create Another Experience
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center">
                <LoadingIndicator />
                <p className="mt-4">Your publication page is still being generated. This may take a few minutes.</p>
                <p className="text-sm text-gray-500 mt-2">Current status: {publicationData?.status || 'processing'}</p>
              </div>
            )}
          </>
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default PublicationPreviewPage;
