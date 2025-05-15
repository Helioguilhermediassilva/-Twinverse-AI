import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'

const MusicPlayerPage = () => {
  const { musicId } = useParams()
  const [musicData, setMusicData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [pollingInterval, setPollingInterval] = useState(null)

  // Função para buscar status da música
  const fetchMusicStatus = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/music/${musicId}`)
      setMusicData(response.data)
      
      // Se a música estiver pronta, parar de verificar
      if (response.data.status === 'completed') {
        if (pollingInterval) {
          clearInterval(pollingInterval)
          setPollingInterval(null)
        }
      }
    } catch (err) {
      setError('Erro ao buscar informações da música')
      console.error('Erro:', err)
      
      // Parar de verificar em caso de erro
      if (pollingInterval) {
        clearInterval(pollingInterval)
        setPollingInterval(null)
      }
    } finally {
      setLoading(false)
    }
  }

  // Iniciar verificação quando o componente montar
  useEffect(() => {
    fetchMusicStatus()
    
    // Verificar status a cada 5 segundos se estiver em processamento
    const interval = setInterval(fetchMusicStatus, 5000)
    setPollingInterval(interval)
    
    // Limpar intervalo quando o componente desmontar
    return () => {
      if (interval) {
        clearInterval(interval)
      }
    }
  }, [musicId])

  // Renderizar estado de carregamento
  if (loading) {
    return (
      <div className="container mx-auto py-8 px-4 text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-purple-500 mx-auto mb-4"></div>
        <h2 className="text-2xl font-bold">Carregando sua música...</h2>
      </div>
    )
  }

  // Renderizar erro
  if (error) {
    return (
      <div className="container mx-auto py-8 px-4 text-center">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded max-w-lg mx-auto">
          <p>{error}</p>
        </div>
        <Link to="/create" className="mt-6 inline-block text-purple-600 hover:underline">
          Voltar e tentar novamente
        </Link>
      </div>
    )
  }

  // Renderizar música em processamento
  if (musicData && musicData.status === 'processing') {
    return (
      <div className="container mx-auto py-8 px-4 text-center">
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
          <div className="animate-pulse flex flex-col items-center">
            <div className="rounded-full bg-purple-200 h-24 w-24 mb-4"></div>
            <div className="h-4 bg-purple-200 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-purple-200 rounded w-1/2"></div>
          </div>
          
          <h2 className="text-2xl font-bold mt-6">Sua música está sendo criada</h2>
          <p className="text-gray-600 mt-2">
            Nossa IA está trabalhando na sua música original. Isso pode levar alguns minutos.
          </p>
          
          <div className="mt-6 w-full bg-gray-200 rounded-full h-2.5">
            <div className="bg-purple-600 h-2.5 rounded-full w-3/4 animate-[pulse_2s_ease-in-out_infinite]"></div>
          </div>
          
          <p className="text-sm text-gray-500 mt-4">
            Não feche esta página. Você será redirecionado automaticamente quando sua música estiver pronta.
          </p>
        </div>
      </div>
    )
  }

  // Renderizar música pronta
  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-center mb-6">Sua Música Original</h1>
        
        <div className="bg-gradient-to-r from-purple-100 to-blue-100 p-4 rounded-lg mb-6">
          <p className="text-center text-lg italic">"{musicData.phrase}"</p>
        </div>
        
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-2">Ouça sua criação</h2>
          <audio 
            controls 
            className="w-full" 
            src={`http://localhost:8000${musicData.music_url}`}
          >
            Seu navegador não suporta o elemento de áudio.
          </audio>
        </div>
        
        <div className="flex justify-center space-x-4">
          <a 
            href={`http://localhost:8000${musicData.music_url}`} 
            download={`twinverse_music.mp3`}
            className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 transition-colors"
          >
            Baixar Música
          </a>
          
          <Link 
            to="/create" 
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Criar Nova Música
          </Link>
        </div>
        
        <div className="mt-8 pt-6 border-t border-gray-200">
          <h3 className="text-lg font-semibold mb-2">Compartilhar</h3>
          <div className="flex justify-center space-x-4">
            <button className="text-blue-600 hover:text-blue-800">
              <span className="sr-only">Facebook</span>
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" />
              </svg>
            </button>
            <button className="text-blue-400 hover:text-blue-600">
              <span className="sr-only">Twitter</span>
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
              </svg>
            </button>
            <button className="text-red-600 hover:text-red-800">
              <span className="sr-only">YouTube</span>
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MusicPlayerPage
