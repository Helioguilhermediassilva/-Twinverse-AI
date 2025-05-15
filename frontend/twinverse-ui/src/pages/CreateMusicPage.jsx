import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const CreateMusicPage = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    phrase: '',
    genre: '',
    emotion: '',
  })
  const [voiceFile, setVoiceFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value,
    })
  }

  const handleFileChange = (e) => {
    setVoiceFile(e.target.files[0])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      // Validar entrada
      if (!formData.phrase.trim()) {
        throw new Error('Por favor, insira uma frase criativa')
      }

      // Criar FormData para envio
      const submitData = new FormData()
      submitData.append('phrase', formData.phrase)
      if (formData.genre) submitData.append('genre', formData.genre)
      if (formData.emotion) submitData.append('emotion', formData.emotion)
      if (voiceFile) submitData.append('voice_file', voiceFile)

      // Enviar para a API
      const response = await axios.post('http://localhost:8000/api/music/create', submitData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      // Redirecionar para a página do player com o ID da música
      navigate(`/player/${response.data.id}`)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Ocorreu um erro ao criar a música')
      console.error('Erro ao criar música:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold text-center mb-8">Crie Sua Música Original</h1>
      
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label htmlFor="phrase" className="block text-gray-700 font-bold mb-2">
              Frase Criativa *
            </label>
            <textarea
              id="phrase"
              name="phrase"
              value={formData.phrase}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              rows="3"
              placeholder="Digite uma frase criativa que inspirará sua música..."
              required
            />
            <p className="text-sm text-gray-500 mt-1">
              Esta frase será a base para toda a sua experiência musical.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <label htmlFor="genre" className="block text-gray-700 font-bold mb-2">
                Gênero Musical (opcional)
              </label>
              <select
                id="genre"
                name="genre"
                value={formData.genre}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="">Selecione um gênero</option>
                <option value="pop">Pop</option>
                <option value="rock">Rock</option>
                <option value="rap">Rap/Hip-Hop</option>
                <option value="eletronica">Eletrônica</option>
                <option value="samba">Samba</option>
                <option value="mpb">MPB</option>
                <option value="funk">Funk</option>
                <option value="jazz">Jazz</option>
                <option value="classica">Clássica</option>
              </select>
            </div>
            
            <div>
              <label htmlFor="emotion" className="block text-gray-700 font-bold mb-2">
                Emoção Principal (opcional)
              </label>
              <select
                id="emotion"
                name="emotion"
                value={formData.emotion}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="">Selecione uma emoção</option>
                <option value="alegria">Alegria</option>
                <option value="tristeza">Tristeza</option>
                <option value="raiva">Raiva</option>
                <option value="medo">Medo</option>
                <option value="amor">Amor</option>
                <option value="esperanca">Esperança</option>
                <option value="nostalgia">Nostalgia</option>
                <option value="empolgacao">Empolgação</option>
              </select>
            </div>
          </div>
          
          <div className="mb-6">
            <label htmlFor="voice_file" className="block text-gray-700 font-bold mb-2">
              Sua Voz (opcional)
            </label>
            <input
              type="file"
              id="voice_file"
              name="voice_file"
              onChange={handleFileChange}
              accept="audio/*"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            <p className="text-sm text-gray-500 mt-1">
              Envie um arquivo de áudio com sua voz para personalizar a música.
            </p>
          </div>
          
          <div className="flex justify-center">
            <button
              type="submit"
              disabled={isLoading}
              className="bg-gradient-to-r from-purple-600 to-blue-500 text-white font-bold py-3 px-6 rounded-full hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {isLoading ? 'Criando sua música...' : 'Criar Música Original'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateMusicPage
