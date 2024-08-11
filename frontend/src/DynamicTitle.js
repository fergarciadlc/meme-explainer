import React, { useState, useEffect } from 'react';

const titles = [
  "Meme Explainer",
  "Ah yes, true comedy",
  "Welcome, humor detective!",
  "Ah, nothing like a good laugh… followed by a lengthy explanation.",
  "Comedy crisis detected!",
  "Welcome to the Comedy Breakdown Service!"
];

const subtitles = [
  "So, you didn't get the joke? Don't worry, I got you.",
  "Ready to overanalyze the punchline?",
  "What humor enigma can I solve for you today?",
  "What needs our critical attention?",
  "What's on your mind?",
  "What punchline puzzle do you need to solve today?"
];

const DynamicTitle = () => {
  const [titleIndex, setTitleIndex] = useState(0);
  const [subtitleIndex, setSubtitleIndex] = useState(0);
  const [fadeTitle, setFadeTitle] = useState(false);
  const [fadeSubtitle, setFadeSubtitle] = useState(false);

  useEffect(() => {
    const subtitleInterval = setInterval(() => {
      setFadeSubtitle(true);
      setTimeout(() => {
        setSubtitleIndex((prevIndex) => (prevIndex + 1) % subtitles.length);
        setFadeSubtitle(false);
      }, 500); // Wait for fade out before changing text
    }, 16000); // Change subtitle every 16 seconds

    const titleInterval = setInterval(() => {
      setFadeTitle(true);
      setTimeout(() => {
        setTitleIndex((prevIndex) => (prevIndex + 1) % titles.length);
        setFadeTitle(false);
      }, 500); // Wait for fade out before changing text
    }, 50000); // Change title every 50 seconds

    return () => {
      clearInterval(subtitleInterval);
      clearInterval(titleInterval);
    };
  }, []);

  return (
    <div className="text-center">
      <h1 
        className={`text-4xl font-bold text-gray-900 transition-opacity duration-500 ${fadeTitle ? 'opacity-0' : 'opacity-100'}`}
      >
        {titles[titleIndex]}
      </h1>
      <p 
        className={`mt-3 text-xl text-gray-600 transition-opacity duration-500 ${fadeSubtitle ? 'opacity-0' : 'opacity-100'}`}
      >
        {subtitles[subtitleIndex]}
      </p>
    </div>
  );
};

export default DynamicTitle;