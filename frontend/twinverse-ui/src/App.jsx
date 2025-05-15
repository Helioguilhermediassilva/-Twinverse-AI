import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import CreateMusicPage from './pages/CreateMusicPage'
import MusicPlayerPage from './pages/MusicPlayerPage'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/create" element={<CreateMusicPage />} />
          <Route path="/player/:musicId" element={<MusicPlayerPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default App
