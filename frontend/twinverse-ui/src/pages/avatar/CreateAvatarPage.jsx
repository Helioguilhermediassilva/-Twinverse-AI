import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import AvatarPreview from '../components/avatar/AvatarPreview';
import AvatarStyleSelector from '../components/avatar/AvatarStyleSelector';
import VisualDescriptionForm from '../components/avatar/VisualDescriptionForm';
import ImageUploader from '../components/avatar/ImageUploader';
import LoadingIndicator from '../components/LoadingIndicator';
import ErrorMessage from '../components/ErrorMessage';
import { createAvatar, getAvatarStatus } from '../services/avatarService';

const CreateAvatarPage = () => {
  const { musicId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [avatarId, setAvatarId] = useState(null);
  const [processingStatus, setProcessingStatus] = useState(null);
  
  const [visualDescription, setVisualDescription] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('realistic');
  const [imageFile, setImageFile] = useState(null);
  
  // Check avatar processing status
  useEffect(() => {
    let statusInterval;
    
    if (avatarId && processingStatus !== 'completed') {
      statusInterval = setInterval(async () => {
        try {
          const status = await getAvatarStatus(avatarId);
          setProcessingStatus(status.status);
          
          if (status.status === 'completed') {
            clearInterval(statusInterval);
            // Navigate to next step or preview
            navigate(`/avatar/${avatarId}/preview`);
          }
        } catch (err) {
          console.error('Error checking avatar status:', err);
        }
      }, 5000); // Check every 5 seconds
    }
    
    return () => {
      if (statusInterval) clearInterval(statusInterval);
    };
  }, [avatarId, processingStatus, navigate]);
  
  const handleStyleChange = (style) => {
    setSelectedStyle(style);
  };
  
  const handleDescriptionChange = (description) => {
    setVisualDescription(description);
  };
  
  const handleImageUpload = (file) => {
    setImageFile(file);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Validate inputs
      if (!visualDescription && !imageFile) {
        throw new Error('Please provide either a visual description or upload an image');
      }
      
      if (!musicId) {
        throw new Error('Music ID is required');
      }
      
      // Create form data
      const formData = new FormData();
      formData.append('music_id', musicId);
      formData.append('style', selectedStyle);
      
      if (visualDescription) {
        formData.append('visual_description', visualDescription);
      }
      
      if (imageFile) {
        formData.append('image_file', imageFile);
      }
      
      // Submit to API
      const response = await createAvatar(formData);
      setAvatarId(response.id);
      setProcessingStatus(response.status);
      
    } catch (err) {
      setError(err.message || 'Error creating avatar');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-center">Create Your Digital Avatar</h1>
        
        {error && <ErrorMessage message={error} />}
        
        {avatarId && processingStatus === 'processing' ? (
          <div className="text-center">
            <LoadingIndicator />
            <p className="mt-4">Creating your avatar... This may take a few minutes.</p>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-6">
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <h2 className="text-xl font-semibold mb-4">Choose Avatar Style</h2>
                <AvatarStyleSelector 
                  selectedStyle={selectedStyle} 
                  onStyleChange={handleStyleChange} 
                />
              </div>
              
              <div className="mb-6">
                <h2 className="text-xl font-semibold mb-4">Describe Your Avatar</h2>
                <VisualDescriptionForm 
                  description={visualDescription} 
                  onDescriptionChange={handleDescriptionChange} 
                />
              </div>
              
              <div className="mb-6">
                <h2 className="text-xl font-semibold mb-4">Or Upload Your Image</h2>
                <ImageUploader onImageUpload={handleImageUpload} />
              </div>
              
              <div className="flex justify-center mt-8">
                <button 
                  type="submit" 
                  className="btn-primary text-lg px-8 py-3"
                  disabled={loading}
                >
                  {loading ? 'Creating...' : 'Create Avatar'}
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

export default CreateAvatarPage;
