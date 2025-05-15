import React from 'react'
import { Link } from 'react-router-dom'

const HomePage = () => {
  return (
    <div className="container mx-auto py-8 px-4">
      <section className="text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-blue-500">
          Twinverse AI
        </h1>
        <p className="text-xl md:text-2xl text-gray-700 max-w-3xl mx-auto">
          Transforme frases criativas em músicas originais, avatares personalizados, 
          curtas-metragens e páginas interativas.
        </p>
        <div className="mt-8">
          <Link 
            to="/create" 
            className="bg-gradient-to-r from-purple-600 to-blue-500 text-white font-bold py-3 px-8 rounded-full hover:opacity-90 transition-opacity inline-block"
          >
            Criar Música Original
          </Link>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        <div className="bg-white p-6 rounded-lg shadow-md text-center">
          <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 mx-auto mb-4">
            <span className="text-2xl">🎵</span>
          </div>
          <h3 className="text-xl font-bold mb-2">Música Original</h3>
          <p className="text-gray-600">
            Transforme sua frase em uma música completa com letra e melodia.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md text-center opacity-60">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 mx-auto mb-4">
            <span className="text-2xl">👤</span>
          </div>
          <h3 className="text-xl font-bold mb-2">Avatar Digital</h3>
          <p className="text-gray-600">
            Crie um avatar personalizado que representa sua identidade criativa.
          </p>
          <span className="text-xs text-gray-500 mt-2 inline-block">Em breve</span>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md text-center opacity-60">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center text-green-600 mx-auto mb-4">
            <span className="text-2xl">🎬</span>
          </div>
          <h3 className="text-xl font-bold mb-2">Curta-Metragem</h3>
          <p className="text-gray-600">
            Transforme sua música em um curta-metragem com roteiro e animação.
          </p>
          <span className="text-xs text-gray-500 mt-2 inline-block">Em breve</span>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md text-center opacity-60">
          <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center text-yellow-600 mx-auto mb-4">
            <span className="text-2xl">🌐</span>
          </div>
          <h3 className="text-xl font-bold mb-2">Página Interativa</h3>
          <p className="text-gray-600">
            Publique e compartilhe sua experiência artística completa.
          </p>
          <span className="text-xs text-gray-500 mt-2 inline-block">Em breve</span>
        </div>
      </section>

      <section className="bg-gray-100 p-8 rounded-lg mb-16">
        <h2 className="text-2xl font-bold mb-4 text-center">Como Funciona</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 bg-purple-500 text-white rounded-full flex items-center justify-center font-bold mb-4">1</div>
            <h3 className="text-lg font-semibold mb-2">Insira sua frase criativa</h3>
            <p className="text-center text-gray-600">
              Digite uma frase que inspire sua criação artística.
            </p>
          </div>
          
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 bg-purple-500 text-white rounded-full flex items-center justify-center font-bold mb-4">2</div>
            <h3 className="text-lg font-semibold mb-2">Personalize sua experiência</h3>
            <p className="text-center text-gray-600">
              Escolha gênero musical, emoção e adicione sua própria voz.
            </p>
          </div>
          
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 bg-purple-500 text-white rounded-full flex items-center justify-center font-bold mb-4">3</div>
            <h3 className="text-lg font-semibold mb-2">Receba sua música original</h3>
            <p className="text-center text-gray-600">
              Nossa IA transforma sua frase em uma música completa e única.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
