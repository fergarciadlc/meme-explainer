import React, { useState, useEffect } from 'react';
import { Upload, Send } from 'lucide-react';
import DynamicTitle from './DynamicTitle';

// Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL;

// API endpoints
const ENDPOINTS = {
  EXPLAIN_IMAGE: '/explain/image',
  EXPLAIN_TEXT: '/explain/text'
};

// API functions
const explainImage = async (imageFile, lang) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  const response = await fetch(`${API_BASE_URL}${ENDPOINTS.EXPLAIN_IMAGE}?lang=${lang}`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) throw new Error('API request failed');
  return response.json();
};

const explainText = async (text, lang) => {
  const response = await fetch(`${API_BASE_URL}${ENDPOINTS.EXPLAIN_TEXT}?lang=${lang}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error('API request failed');
  return response.json();
};

const TypewriterEffect = ({ text }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < text.length) {
      const timer = setTimeout(() => {
        setDisplayedText((prevText) => prevText + text[index]);
        setIndex((prevIndex) => prevIndex + 1);
      }, 5);

      return () => clearTimeout(timer);
    }
  }, [index, text]);

  return <p className="text-gray-600">{displayedText}</p>;
};

// Main component
const MemeExplainer = () => {
  const [memeText, setMemeText] = useState('');
  const [memeImage, setMemeImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [explanation, setExplanation] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [model, setModel] = useState('');
  const [language, setLanguage] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('en');

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setMemeImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const explainMeme = async () => {
    setIsLoading(true);
    setExplanation('');
    setError(null);
    setModel('');
    setLanguage('');
    try {
      let data;
      if (memeImage) {
        data = await explainImage(memeImage, selectedLanguage);
      } else if (memeText) {
        data = await explainText(memeText, selectedLanguage);
      } else {
        throw new Error('Please provide either text or an image');
      }
      setExplanation(data.explanation);
      setModel(data.model);
      setLanguage(data.language);
    } catch (error) {
      setError(`An error occurred: ${error.message}`);
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl w-full space-y-8">
        <DynamicTitle />

        <div className="bg-white shadow-xl rounded-lg overflow-hidden">
          <div className="p-6 space-y-6">
            <div className="flex flex-col lg:flex-row gap-6">
              <div className="w-full lg:w-1/2 space-y-4">
                <textarea
                  className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  rows={4}
                  value={memeText}
                  onChange={(e) => setMemeText(e.target.value)}
                  placeholder="Type your meme text here..."
                />

                <label className="flex items-center justify-center w-full p-4 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-500 transition-colors">
                  <input type="file" className="hidden" onChange={handleImageUpload} accept="image/*" />
                  <Upload className="mr-2 text-gray-500" />
                  <span className="text-gray-500">Upload Meme Image</span>
                </label>

                {imagePreview && (
                  <div className="mt-4">
                    <img src={imagePreview} alt="Uploaded meme" className="max-w-full h-auto rounded-lg" />
                  </div>
                )}

                {/* Language selector moved here and styled to be smaller and subtle */}
                <div className="flex items-center justify-end space-x-2 text-sm">
                  <label htmlFor="language-select" className="text-gray-500">
                    Explanation Language:
                  </label>
                  <select
                    id="language-select"
                    value={selectedLanguage}
                    onChange={(e) => setSelectedLanguage(e.target.value)}
                    className="py-1 px-2 border border-gray-300 rounded-md text-gray-700 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="en">English</option>
                    <option value="es">Español</option>
                  </select>
                </div>

                <button
              className="w-full bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-200 flex items-center justify-center"
              onClick={explainMeme}
              disabled={isLoading || (!memeText && !memeImage)}
            >
              {isLoading ? (
                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
              ) : (
                <Send className="mr-2" />
              )}
              {isLoading ? 'Explaining...' : 'Explain Meme'}
            </button>
          </div>

              <div className="w-full lg:w-1/2">
                {explanation ? (
                  <div className="bg-gray-50 rounded-lg p-4 h-full relative">
                    {(model || language) && (
                      <div className="absolute top-2 right-2 flex space-x-2">
                        {model && (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            Model: {model}
                          </span>
                        )}
                        {language && (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Lang: {language}
                          </span>
                        )}
                      </div>
                    )}
                    <h2 className="text-xl font-semibold mb-2 text-gray-800">Explanation:</h2>
                    <TypewriterEffect text={explanation} />
                  </div>
                ) : (
                  <div className="bg-gray-50 rounded-lg p-4 h-full flex items-center justify-center">
                    <p className="text-gray-500 text-center">Your meme explanation will appear here</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {error && (
            <div className="bg-red-100 border-t-4 border-red-500 rounded-b text-red-900 px-4 py-3 shadow-md" role="alert">
              <div className="flex">
                <div className="py-1"><svg className="fill-current h-6 w-6 text-red-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z" /></svg></div>
                <div>
                  <p className="font-bold">Error</p>
                  <p className="text-sm">{error}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MemeExplainer;