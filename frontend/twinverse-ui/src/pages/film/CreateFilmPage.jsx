import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import LoadingIndicator from '../components/LoadingIndicator';
import ErrorMessage from '../components/ErrorMessage';
import { createFilm, getFilmStatus } from '../services/filmService';

const CreateFilmPage = () => {
  const { musicId, avatarId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filmId, setFilmId] = useState(null);
  const [processingStatus, setProcessingStatus] = useState(null);
  
  // Check film processing status
  useEffect(() => {
    let statusInterval;
    
    if (filmId && processingStatus !== 'completed') {
      statusInterval = setInterval(async () => {
        try {
          const status = await getFilmStatus(filmId);
          setProcessingStatus(status.status);
          
          if (status.status === 'completed') {
            clearInterval(statusInterval);
            // Navigate to film preview
            navigate(`/film/${filmId}/preview`);
          }
        } catch (err) {
          console.error('Error checking film status:', err);
        }
      }, 5000); // Check every 5 seconds
    }
    
    return () => {
      if (statusInterval) clearInterval(statusInterval);
    };
  }, [filmId, processingStatus, navigate]);
  
  const handleCreateFilm = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Validate inputs
      if (!musicId || !avatarId) {
        throw new Error('Music ID and Avatar ID are required');
      }
      
      // Create form data
      const formData = new FormData();
      formData.append('music_id', musicId);
      formData.append('avatar_id', avatarId);
      
      // Submit to API
      const response = await createFilm(formData);
      setFilmId(response.id);
      setProcessingStatus(response.status);
      
    } catch (err) {
      setError(err.message || 'Error creating film');
    } finally {
      setLoading(false);
    }
  };
  
  // Auto-start film creation when page loads
  useEffect(() => {
    if (!filmId && !loading && !error) {
      handleCreateFilm();
    }
  }, [filmId, loading, error]);
  
  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-center">Creating Your Short Film</h1>
        
        {error && <ErrorMessage message={error} />}
        
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          {loading || (filmId && processingStatus === 'processing') ? (
            <>
              <LoadingIndicator />
              <div className="mt-6">
                <h2 className="text-2xl font-semibold mb-4">Your film is being created</h2>
                <p className="text-gray-600 mb-4">
                  We're generating a unique short film based on your music and avatar.
                  This process involves several steps:
                </p>
                
                <div className="max-w-md mx-auto text-left">
                  <div className="flex items-center mb-3">
                    <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-white font-bold mr-3">1</div>
                    <p>Creating a screenplay based on your music</p>
                  </div>
                  <div className="flex items-center mb-3">
                    <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-white font-bold mr-3">2</div>
                    <p>Generating a storyboard with key scenes</p>
                  </div>
                  <div className="flex items-center mb-3">
                    <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-white font-bold mr-3">3</div>
                    <p>Producing video scenes with AI</p>
                  </div>
                  <div className="flex items-center">
                    <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-white font-bold mr-3">4</div>
                    <p>Combining everything into your final film</p>
                  </div>
                </div>
                
                <p className="mt-6 text-sm text-gray-500">
                  This process may take 5-10 minutes. Please don't close this page.
                </p>
              </div>
            </>
          ) : (
            <>
              <h2 className="text-2xl font-semibold mb-4">Ready to create your film?</h2>
              <p className="text-gray-600 mb-6">
                We'll generate a unique short film based on your music and avatar.
                This process may take several minutes.
              </p>
              <button 
                onClick={handleCreateFilm}
                className="btn-primary text-lg px-8 py-3"
              >
                Start Film Creation
              </button>
            </>
          )}
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default CreateFilmPage;
