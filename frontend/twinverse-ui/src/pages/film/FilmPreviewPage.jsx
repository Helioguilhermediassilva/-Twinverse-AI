import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import FilmPlayer from '../components/film/FilmPlayer';
import ScreenplayViewer from '../components/film/ScreenplayViewer';
import StoryboardViewer from '../components/film/StoryboardViewer';
import LoadingIndicator from '../components/LoadingIndicator';
import ErrorMessage from '../components/ErrorMessage';
import { getFilmStatus } from '../services/filmService';

const FilmPreviewPage = () => {
  const { filmId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filmData, setFilmData] = useState(null);
  const [activeTab, setActiveTab] = useState('film');
  
  useEffect(() => {
    const fetchFilmData = async () => {
      try {
        const data = await getFilmStatus(filmId);
        setFilmData(data);
        setLoading(false);
      } catch (err) {
        setError(err.message || 'Error loading film');
        setLoading(false);
      }
    };
    
    fetchFilmData();
  }, [filmId]);
  
  const handleContinue = () => {
    // Extract music_id and avatar_id from filmData
    const { music_id, avatar_id } = filmData;
    
    // Navigate to publication creation page
    navigate(`/publication/create/${music_id}/${avatar_id}/${filmId}`);
  };
  
  const handleRegenerate = () => {
    // Extract music_id and avatar_id from filmData
    const { music_id, avatar_id } = filmData;
    
    // Navigate back to film creation page
    navigate(`/film/create/${music_id}/${avatar_id}`);
  };
  
  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-center">Your Short Film</h1>
        
        {error && <ErrorMessage message={error} />}
        
        {loading ? (
          <div className="text-center">
            <LoadingIndicator />
            <p className="mt-4">Loading your film...</p>
          </div>
        ) : (
          <>
            {filmData && filmData.status === 'completed' ? (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="mb-6">
                  <div className="flex border-b border-gray-200">
                    <button
                      className={`px-4 py-2 font-medium ${activeTab === 'film' ? 'text-purple-600 border-b-2 border-purple-600' : 'text-gray-500'}`}
                      onClick={() => setActiveTab('film')}
                    >
                      Film
                    </button>
                    <button
                      className={`px-4 py-2 font-medium ${activeTab === 'screenplay' ? 'text-purple-600 border-b-2 border-purple-600' : 'text-gray-500'}`}
                      onClick={() => setActiveTab('screenplay')}
                    >
                      Screenplay
                    </button>
                    <button
                      className={`px-4 py-2 font-medium ${activeTab === 'storyboard' ? 'text-purple-600 border-b-2 border-purple-600' : 'text-gray-500'}`}
                      onClick={() => setActiveTab('storyboard')}
                    >
                      Storyboard
                    </button>
                  </div>
                  
                  <div className="mt-4">
                    {activeTab === 'film' && (
                      <FilmPlayer videoUrl={filmData.film_url} />
                    )}
                    
                    {activeTab === 'screenplay' && (
                      <ScreenplayViewer screenplayUrl={filmData.screenplay_url} />
                    )}
                    
                    {activeTab === 'storyboard' && (
                      <StoryboardViewer storyboardUrl={filmData.storyboard_url} />
                    )}
                  </div>
                </div>
                
                <div className="flex justify-center gap-4 mt-8">
                  <button 
                    onClick={handleRegenerate}
                    className="btn-secondary text-lg px-6 py-2"
                  >
                    Regenerate Film
                  </button>
                  <button 
                    onClick={handleContinue}
                    className="btn-primary text-lg px-8 py-2"
                  >
                    Continue to Publication
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center">
                <LoadingIndicator />
                <p className="mt-4">Your film is still being generated. This may take a few minutes.</p>
                <p className="text-sm text-gray-500 mt-2">Current status: {filmData?.status || 'processing'}</p>
              </div>
            )}
          </>
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default FilmPreviewPage;
