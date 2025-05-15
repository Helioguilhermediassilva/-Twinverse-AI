import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import AvatarViewer from '../components/avatar/AvatarViewer';
import LoadingIndicator from '../components/LoadingIndicator';
import ErrorMessage from '../components/ErrorMessage';
import { getAvatarStatus } from '../services/avatarService';

const AvatarPreviewPage = () => {
  const { avatarId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [avatarData, setAvatarData] = useState(null);
  
  useEffect(() => {
    const fetchAvatarData = async () => {
      try {
        const data = await getAvatarStatus(avatarId);
        setAvatarData(data);
        setLoading(false);
      } catch (err) {
        setError(err.message || 'Error loading avatar');
        setLoading(false);
      }
    };
    
    fetchAvatarData();
  }, [avatarId]);
  
  const handleContinue = () => {
    // Navigate to film creation page
    navigate(`/film/create/${avatarData.music_id}/${avatarId}`);
  };
  
  const handleRegenerate = () => {
    // Navigate back to avatar creation page
    navigate(`/avatar/create/${avatarData.music_id}`);
  };
  
  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-center">Your Digital Avatar</h1>
        
        {error && <ErrorMessage message={error} />}
        
        {loading ? (
          <div className="text-center">
            <LoadingIndicator />
            <p className="mt-4">Loading your avatar...</p>
          </div>
        ) : (
          <>
            {avatarData && avatarData.status === 'completed' ? (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="mb-6">
                  <h2 className="text-xl font-semibold mb-4 text-center">Avatar Preview</h2>
                  <AvatarViewer 
                    videoUrl={avatarData.avatar_video_url}
                    modelUrl={avatarData.avatar_model_url}
                  />
                </div>
                
                <div className="flex justify-center gap-4 mt-8">
                  <button 
                    onClick={handleRegenerate}
                    className="btn-secondary text-lg px-6 py-2"
                  >
                    Regenerate Avatar
                  </button>
                  <button 
                    onClick={handleContinue}
                    className="btn-primary text-lg px-8 py-2"
                  >
                    Continue to Film Creation
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center">
                <LoadingIndicator />
                <p className="mt-4">Your avatar is still being generated. This may take a few minutes.</p>
                <p className="text-sm text-gray-500 mt-2">Current status: {avatarData?.status || 'processing'}</p>
              </div>
            )}
          </>
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default AvatarPreviewPage;
