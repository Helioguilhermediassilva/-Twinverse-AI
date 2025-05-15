# Arquitetura do Twinverse-AI

## Visão Geral

O Twinverse-AI é uma plataforma multimodal de IA que transforma frases criativas em experiências artísticas completas. O MVP inicial foca na fase de música personalizada, com uma arquitetura modular que permitirá a integração futura das fases de avatar, curta-metragem e página de publicação.

## Arquitetura Técnica

### Diagrama de Alto Nível

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  Cliente (React) | <-> | Backend (FastAPI)| <-> |  Serviços de IA  |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
                                  ^
                                  |
                                  v
                         +------------------+
                         |                  |
                         |   Armazenamento  |
                         |                  |
                         +------------------+
```

## Componentes Principais

### Backend (FastAPI)

#### Módulos:

1. **Core**
   - Configuração da aplicação
   - Gerenciamento de dependências
   - Middleware e utilitários

2. **API**
   - Endpoints RESTful
   - Validação de entrada
   - Autenticação (preparado para futuras implementações)

3. **Serviços**
   - **Interpretação de Frase**
     - Análise de emoção dominante
     - Extração de palavras-chave
     - Sugestão de gênero musical

   - **Geração de Letra**
     - Criação de estrutura musical (versos, refrão)
     - Garantia de coerência temática
     - Aplicação de regras de composição

   - **Geração de Música**
     - Integração com Suno AI / Boomy
     - Processamento de melodia instrumental
     - Formatação e armazenamento de áudio

   - **Processamento de Voz**
     - Integração com ElevenLabs / Respeecher
     - Upload e processamento de voz do usuário
     - Aplicação de voz à música

4. **Modelos**
   - Esquemas de dados
   - Entidades de negócio
   - DTOs (Data Transfer Objects)

5. **Repositórios**
   - Acesso a dados
   - Armazenamento de arquivos
   - Cache (opcional)

### Frontend (React)

#### Componentes:

1. **Páginas**
   - Página inicial
   - Criação de música
   - Reprodução e compartilhamento
   - Perfil do usuário (preparado para futuras implementações)

2. **Componentes**
   - Formulário de entrada de frase
   - Seleção de gênero e emoção
   - Upload/gravação de voz
   - Player de música
   - Visualização de progresso

3. **Serviços**
   - Comunicação com API
   - Gerenciamento de estado
   - Manipulação de áudio

4. **Utilitários**
   - Formatação
   - Validação
   - Manipulação de arquivos

### Integrações Externas

1. **OpenAI GPT-4o**
   - Interpretação de frases
   - Geração de letras de música
   - Análise de emoção

2. **Suno AI / Boomy**
   - Geração de melodia instrumental
   - Criação de base musical

3. **ElevenLabs / Respeecher**
   - Síntese de voz
   - Clonagem de voz do usuário

## Fluxo de Dados (MVP - Fase Música)

1. Usuário insere frase criativa, gênero (opcional), emoção (opcional) e voz (opcional)
2. Backend interpreta a frase usando OpenAI GPT-4o para identificar emoção, palavras-chave e gênero sugerido
3. Backend gera letra de música com estrutura definida
4. Backend solicita melodia instrumental via Suno AI/Boomy
5. Backend processa voz do usuário ou gera voz sintética via ElevenLabs/Respeecher
6. Backend combina melodia e voz para criar música final
7. Frontend recebe e reproduz a música finalizada
8. Usuário pode compartilhar ou baixar a música

## Armazenamento

1. **Arquivos Temporários**
   - Uploads de voz do usuário
   - Arquivos intermediários de processamento

2. **Arquivos Persistentes**
   - Músicas finalizadas
   - Metadados de criação

3. **Banco de Dados**
   - Informações do usuário (futuro)
   - Histórico de criações
   - Configurações e preferências

## Considerações de Escalabilidade

1. **Arquitetura Modular**
   - Cada fase (música, avatar, vídeo, publicação) como módulo independente
   - Interfaces bem definidas entre módulos

2. **Processamento Assíncrono**
   - Filas de tarefas para processamento de longa duração
   - Notificações em tempo real sobre progresso

3. **Expansão Futura**
   - Estrutura preparada para integração das fases 2, 3 e 4
   - APIs internas documentadas para facilitar expansão

## Requisitos Técnicos

### Backend
- Python 3.9+
- FastAPI
- Pydantic
- SQLAlchemy (opcional para MVP)
- FFmpeg (processamento de áudio)
- Bibliotecas de cliente para APIs externas

### Frontend
- Node.js 16+
- React 18+
- Vite (build tool)
- Tailwind CSS (estilização)
- React Query (gerenciamento de estado)
- Howler.js (manipulação de áudio)
