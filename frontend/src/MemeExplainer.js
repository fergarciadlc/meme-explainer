import React, { useState } from 'react';
import { Upload, Send } from 'lucide-react';

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
    <div className={`max-w-2xl mx-auto p-6 bg-gray-100 rounded-lg shadow-lg ${error && error.includes('Failed to fetch') ? 'bg-red-100' : ''}`}>
      <h1 className="text-4xl font-bold mb-6 text-center text-blue-600">Meme Explainer</h1>
      
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">Why is this funny?:</label>
        <textarea
          className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          rows={4}
          value={memeText}
          onChange={(e) => setMemeText(e.target.value)}
          placeholder="Type your meme text here..."
        />
      </div>

      <div className="mb-4">
        <label className="flex items-center justify-center w-full p-4 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-500">
          <input type="file" className="hidden" onChange={handleImageUpload} accept="image/*" />
          <Upload className="mr-2" />
          <span>Upload Meme Image</span>
        </label>
      </div>

      {imagePreview && (
        <div className="mb-4">
          <img src={imagePreview} alt="Uploaded meme" className="max-w-full h-auto rounded-lg" />
        </div>
      )}

      <button
        className="w-full bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition duration-200 flex items-center justify-center"
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

      {explanation && (
        <div className="mt-6 p-4 bg-white rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2 text-gray-800">Explanation:</h2>
          <p className="text-gray-600">{explanation}</p>
        </div>
      )}
    </div>
  );
};

export default MemeExplainer;