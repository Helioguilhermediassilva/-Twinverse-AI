# Documentação do Twinverse-AI

## Visão Geral

O Twinverse-AI é uma plataforma multimodal de inteligência artificial que transforma frases criativas em experiências artísticas completas. O MVP atual implementa a primeira fase do projeto: a criação de músicas originais a partir de frases criativas.

## Estrutura do Projeto

```
Twinverse-AI/
├── backend/                  # API FastAPI
│   ├── api/                  # Endpoints da API
│   ├── core/                 # Configurações e utilitários
│   ├── models/               # Esquemas de dados
│   ├── repositories/         # Acesso a dados
│   ├── services/             # Lógica de negócio
│   ├── main.py               # Ponto de entrada da aplicação
│   └── requirements.txt      # Dependências Python
├── frontend/                 # Interface React
│   └── twinverse-ui/         # Aplicação React
│       ├── public/           # Arquivos estáticos
│       ├── src/              # Código-fonte
│       │   ├── components/   # Componentes reutilizáveis
│       │   ├── pages/        # Páginas da aplicação
│       │   ├── services/     # Serviços e APIs
│       │   └── utils/        # Utilitários
│       ├── package.json      # Dependências Node.js
│       └── vite.config.js    # Configuração do Vite
├── prompts/                  # Prompts para IA
│   └── twinverse_master_prompt.txt
├── arquitetura.md            # Documentação da arquitetura
├── validacao.md              # Validação do MVP
├── README.md                 # Documentação principal
└── LICENSE                   # Licença MIT
```

## Tecnologias Utilizadas

### Backend
- Python 3.9+
- FastAPI
- Pydantic
- OpenAI (GPT-4o)
- Integrações com Suno AI/Boomy e ElevenLabs/Respeecher

### Frontend
- React 18
- Vite
- React Router
- React Query
- Tailwind CSS
- Axios

## Fluxo de Funcionamento

1. O usuário insere uma frase criativa, opcionalmente especificando gênero musical, emoção e enviando um arquivo de voz
2. O backend interpreta a frase para identificar emoção dominante, palavras-chave e gênero musical sugerido
3. O backend gera uma letra de música com estrutura definida (verso, pré-refrão, refrão, etc.)
4. O backend solicita a geração de uma melodia instrumental baseada no estilo e emoção
5. O backend processa a voz do usuário ou gera uma voz sintética para a letra
6. O backend combina a melodia e a voz para criar a música finalizada
7. O frontend exibe a música para o usuário, permitindo reprodução e download

## Configuração e Execução

### Requisitos
- Python 3.9+
- Node.js 16+
- npm ou yarn

### Backend

1. Instalar dependências:
```bash
cd backend
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente:
Crie um arquivo `.env` na pasta `backend` com as seguintes variáveis:
```
OPENAI_API_KEY=sua_chave_api_openai
SUNO_API_KEY=sua_chave_api_suno
ELEVENLABS_API_KEY=sua_chave_api_elevenlabs
```

3. Iniciar o servidor:
```bash
python main.py
```
O servidor estará disponível em `http://localhost:8000`

### Frontend

1. Instalar dependências:
```bash
cd frontend/twinverse-ui
npm install
```

2. Iniciar o servidor de desenvolvimento:
```bash
npm run dev
```
O frontend estará disponível em `http://localhost:5173`

## Próximos Passos

O MVP atual implementa apenas a primeira fase do projeto (música personalizada). As próximas fases incluirão:

1. Geração de avatar digital personalizado
2. Criação de curta-metragem com roteiro, animação e trilha sonora
3. Página de publicação e compartilhamento

## Notas de Implementação

- As integrações com APIs externas (Suno AI, ElevenLabs) estão simuladas no MVP
- Para uma implementação completa, é necessário configurar as chaves de API reais
- O armazenamento de arquivos é local; em produção, considere usar um serviço de armazenamento em nuvem
