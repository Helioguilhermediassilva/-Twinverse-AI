import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import LoadingIndicator from '../components/LoadingIndicator';
import ErrorMessage from '../components/ErrorMessage';
import { createPublication, getPublicationStatus } from '../services/publicationService';

const CreatePublicationPage = () => {
  const { musicId, avatarId, filmId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [publicationId, setPublicationId] = useState(null);
  const [processingStatus, setProcessingStatus] = useState(null);
  const [artistName, setArtistName] = useState('');
  
  // Check publication processing status
  useEffect(() => {
    let statusInterval;
    
    if (publicationId && processingStatus !== 'completed') {
      statusInterval = setInterval(async () => {
        try {
          const status = await getPublicationStatus(publicationId);
          setProcessingStatus(status.status);
          
          if (status.status === 'completed') {
            clearInterval(statusInterval);
            // Navigate to publication preview
            navigate(`/publication/${publicationId}/preview`);
          }
        } catch (err) {
          console.error('Error checking publication status:', err);
        }
      }, 5000); // Check every 5 seconds
    }
    
    return () => {
      if (statusInterval) clearInterval(statusInterval);
    };
  }, [publicationId, processingStatus, navigate]);
  
  const handleArtistNameChange = (e) => {
    setArtistName(e.target.value);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Validate inputs
      if (!musicId || !avatarId || !filmId) {
        throw new Error('Music ID, Avatar ID, and Film ID are required');
      }
      
      // Create form data
      const formData = new FormData();
      formData.append('music_id', musicId);
      formData.append('avatar_id', avatarId);
      formData.append('film_id', filmId);
      
      if (artistName) {
        formData.append('artist_name', artistName);
      }
      
      // Submit to API
      const response = await createPublication(formData);
      setPublicationId(response.id);
      setProcessingStatus(response.status);
      
    } catch (err) {
      setError(err.message || 'Error creating publication');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-center">Create Your Publication Page</h1>
        
        {error && <ErrorMessage message={error} />}
        
        {publicationId && processingStatus === 'processing' ? (
          <div className="text-center">
            <LoadingIndicator />
            <p className="mt-4">Creating your publication page... This may take a few minutes.</p>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-6">
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <h2 className="text-xl font-semibold mb-4">Publication Details</h2>
                
                <div className="mb-4">
                  <label htmlFor="artistName" className="block text-gray-700 mb-2">
                    Artist or Character Name (Optional)
                  </label>
                  <input
                    type="text"
                    id="artistName"
                    className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    placeholder="Enter a name for your artist or character"
                    value={artistName}
                    onChange={handleArtistNameChange}
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    This name will be displayed on your publication page. If left blank, we'll use "Twinverse Artist".
                  </p>
                </div>
              </div>
              
              <div className="mb-6">
                <h2 className="text-xl font-semibold mb-4">Publication Preview</h2>
                <div className="bg-gray-100 p-4 rounded-md">
                  <p className="text-center text-gray-600">
                    Your publication page will include:
                  </p>
                  <ul className="mt-2 space-y-2">
                    <li className="flex items-center">
                      <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                      Your original music
                    </li>
                    <li className="flex items-center">
                      <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                      Your digital avatar
                    </li>
                    <li className="flex items-center">
                      <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                      Your short film
                    </li>
                    <li className="flex items-center">
                      <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                      Social media sharing buttons
                    </li>
                  </ul>
                </div>
              </div>
              
              <div className="flex justify-center mt-8">
                <button 
                  type="submit" 
                  className="btn-primary text-lg px-8 py-3"
                  disabled={loading}
                >
                  {loading ? 'Creating...' : 'Create Publication Page'}
                </button>
              </div>
            </form>
          </div>
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default CreatePublicationPage;
