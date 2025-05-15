import React from 'react'
import { Link } from 'react-router-dom'
import logo from '../assets/twinverse-logo.png'

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-purple-600 to-blue-500 text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="flex items-center space-x-2">
          {/* Placeholder para logo - em produção, usar imagem real */}
          <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center text-purple-600 font-bold">T</div>
          <span className="text-xl font-bold">Twinverse AI</span>
        </Link>
        
        <nav>
          <ul className="flex space-x-6">
            <li>
              <Link to="/" className="hover:text-purple-200 transition-colors">
                Início
              </Link>
            </li>
            <li>
              <Link to="/create" className="hover:text-purple-200 transition-colors">
                Criar Música
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  )
}

export default Header
