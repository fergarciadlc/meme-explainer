import React, { useState, useEffect } from 'react';
import { Upload, Send } from 'lucide-react';

const TypewriterEffect = ({ text }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < text.length) {
      const timer = setTimeout(() => {
        setDisplayedText((prevText) => prevText + text[index]);
        setIndex((prevIndex) => prevIndex + 1);
      }, 7);

      return () => clearTimeout(timer);
    }
  }, [index, text]);

  return <p className="text-gray-600">{displayedText}</p>;
};

const MemeExplainer = () => {
  const [memeText, setMemeText] = useState('');
  const [memeImage, setMemeImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [explanation, setExplanation] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

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
    try {
      let response;
      let data;

      if (memeImage) {
        const formData = new FormData();
        formData.append('file', memeImage);
        response = await fetch('http://localhost:8000/explain/image', {
          method: 'POST',
          body: formData,
        });
      } else if (memeText) {
        response = await fetch('http://localhost:8000/explain/text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: memeText }),
        });
      } else {
        throw new Error('Please provide either text or an image');
      }

      if (!response.ok) {
        throw new Error('API request failed');
      }

      data = await response.json();
      setExplanation(data.explanation);
    } catch (error) {
      setError(`An error occurred: ${error.message}`);
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-10 text-gray-800">Meme Explainer</h1>
        
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="w-full lg:w-1/2 bg-white rounded-lg shadow-md p-6">
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">Enter meme text:</label>
              <textarea
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                rows={4}
                value={memeText}
                onChange={(e) => setMemeText(e.target.value)}
                placeholder="Type your meme text here..."
              />
            </div>

            <div className="mb-6">
              <label className="flex items-center justify-center w-full p-4 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-500 transition-colors">
                <input type="file" className="hidden" onChange={handleImageUpload} accept="image/*" />
                <Upload className="mr-2 text-gray-500" />
                <span className="text-gray-500">Upload Meme Image</span>
              </label>
            </div>

            {imagePreview && (
              <div className="mb-6">
                <img src={imagePreview} alt="Uploaded meme" className="max-w-full h-auto rounded-lg" />
              </div>
            )}

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

            {error && (
              <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                {error}
              </div>
            )}
          </div>

          <div className="w-full lg:w-1/2">
            {explanation ? (
              <div className="bg-white rounded-lg shadow-md p-6 h-full">
                <h2 className="text-xl font-semibold mb-4 text-gray-800">Explanation:</h2>
                <TypewriterEffect text={explanation} />
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-6 h-full flex items-center justify-center">
                <p className="text-gray-500 text-center">Your meme explanation will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MemeExplainer;