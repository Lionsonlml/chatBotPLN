/**
 * Módulo de Conocimiento sobre Videojuegos
 * Contiene información, vocabulario y respuestas relacionadas con videojuegos
 */

// Vocabulario relacionado con videojuegos
export const GAMING_VOCABULARY = {
  // Géneros de videojuegos
  generos: [
    'acción', 'aventura', 'rol', 'estrategia', 'simulación', 'deportes', 'carreras',
    'shooter', 'fps', 'tps', 'mmorpg', 'rpg', 'moba', 'battle royale', 'sandbox',
    'plataformas', 'puzzle', 'roguelike', 'metroidvania', 'survival horror', 'mundo abierto'
  ],
  
  // Plataformas y consolas
  plataformas: [
    'pc', 'playstation', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'xbox', 'xbox 360',
    'xbox one', 'xbox series x', 'nintendo', 'switch', 'wii', 'game boy', '3ds',
    'mobile', 'android', 'ios', 'steam deck', 'vr', 'oculus', 'psvr'
  ],
  
  // Términos técnicos y mecánicas
  terminos_tecnicos: [
    'fps', 'resolución', 'gráficos', 'ray tracing', 'dlss', 'hdr', '4k', '60fps',
    'lag', 'ping', 'servidor', 'online', 'multijugador', 'cooperativo', 'pvp', 'pve',
    'dificultad', 'nivel', 'jefe', 'checkpoint', 'guardado', 'partida', 'campaña'
  ],
  
  // Compañías y desarrolladores
  companias: [
    'nintendo', 'sony', 'microsoft', 'valve', 'epic games', 'ubisoft', 'ea',
    'activision', 'blizzard', 'rockstar', 'bethesda', 'cd projekt red', 'square enix',
    'capcom', 'konami', 'sega', 'bandai namco', 'from software', 'naughty dog'
  ],
  
  // Eventos y competiciones
  eventos: [
    'e3', 'gamescom', 'tokyo game show', 'pax', 'blizzcon', 'the game awards',
    'esports', 'torneo', 'competición', 'mundial', 'liga', 'campeonato'
  ]
};

// Juegos populares con información
export const POPULAR_GAMES = {
  'minecraft': {
    desarrollador: 'Mojang Studios',
    genero: 'Sandbox, Supervivencia',
    plataformas: ['PC', 'Consolas', 'Mobile'],
    descripcion: 'Juego de mundo abierto que permite a los jugadores construir y explorar mundos hechos de bloques.'
  },
  'fortnite': {
    desarrollador: 'Epic Games',
    genero: 'Battle Royale, Shooter',
    plataformas: ['PC', 'Consolas', 'Mobile'],
    descripcion: 'Popular juego battle royale donde 100 jugadores luchan hasta que solo queda uno.'
  },
  'the legend of zelda': {
    desarrollador: 'Nintendo',
    genero: 'Acción-Aventura',
    plataformas: ['Nintendo Switch', 'Consolas Nintendo'],
    descripcion: 'Serie de juegos de aventura que sigue las hazañas de Link en el reino de Hyrule.'
  },
  'call of duty': {
    desarrollador: 'Activision',
    genero: 'FPS, Shooter',
    plataformas: ['PC', 'PlayStation', 'Xbox'],
    descripcion: 'Serie de juegos de disparos en primera persona con modos campaña y multijugador.'
  },
  'fifa': {
    desarrollador: 'EA Sports',
    genero: 'Deportes, Simulación',
    plataformas: ['PC', 'PlayStation', 'Xbox', 'Nintendo Switch'],
    descripcion: 'Simulador de fútbol con licencias oficiales de equipos y jugadores reales.'
  },
  'grand theft auto': {
    desarrollador: 'Rockstar Games',
    genero: 'Acción-Aventura, Mundo Abierto',
    plataformas: ['PC', 'PlayStation', 'Xbox'],
    descripcion: 'Serie de juegos de mundo abierto con narrativas criminales y libertad de exploración.'
  },
  'league of legends': {
    desarrollador: 'Riot Games',
    genero: 'MOBA',
    plataformas: ['PC'],
    descripcion: 'Juego de estrategia en equipo donde dos equipos de campeones se enfrentan.'
  },
  'pokemon': {
    desarrollador: 'Game Freak',
    genero: 'RPG',
    plataformas: ['Consolas Nintendo', 'Mobile'],
    descripcion: 'Serie de juegos donde entrenadores capturan y entrenan criaturas llamadas Pokémon.'
  },
  'dark souls': {
    desarrollador: 'FromSoftware',
    genero: 'RPG de Acción',
    plataformas: ['PC', 'PlayStation', 'Xbox'],
    descripcion: 'Serie conocida por su alta dificultad y combate estratégico.'
  },
  'overwatch': {
    desarrollador: 'Blizzard',
    genero: 'FPS, Hero Shooter',
    plataformas: ['PC', 'PlayStation', 'Xbox', 'Nintendo Switch'],
    descripcion: 'Shooter en equipo con diversos héroes con habilidades únicas.'
  }
};

// Respuestas temáticas sobre videojuegos
export const GAMING_RESPONSES = [
  "Los videojuegos han evolucionado mucho desde Pong y Space Invaders, ¿no crees?",
  "¿Qué opinas de los juegos indie? Algunos como Hollow Knight o Stardew Valley han tenido tanto éxito como los AAA.",
  "La narrativa en los videojuegos ha alcanzado niveles comparables al cine y la literatura.",
  "Los esports se han convertido en un fenómeno global con millones de espectadores.",
  "La realidad virtual está cambiando la forma en que experimentamos los videojuegos.",
  "¿Prefieres jugar en consola o PC? Es un debate que nunca termina en la comunidad gaming.",
  "Los juegos de mundo abierto ofrecen una libertad increíble, pero a veces pueden sentirse abrumadores.",
  "Los roguelikes son adictivos por su naturaleza de 'una partida más' y la aleatoriedad.",
  "Los juegos multijugador competitivos como League of Legends o CS:GO tienen curvas de aprendizaje muy pronunciadas.",
  "La accesibilidad en los videojuegos ha mejorado mucho, permitiendo que más personas puedan disfrutarlos."
];

// Respuestas para mensajes fuera del tema de videojuegos
export const OFF_TOPIC_RESPONSES = [
  "Estamos hablando de videojuegos. Si tienes alguna pregunta o comentario sobre juegos, consolas, o la industria gaming, estaré encantado de seguir la conversación.",
  "Parece que nos estamos desviando del tema de los videojuegos. ¿Te gustaría que volvamos a hablar sobre algún aspecto del mundo gaming?",
  "Como especialista en videojuegos, puedo ofrecerte información sobre juegos, plataformas, géneros y más. ¿Hay algo específico del mundo gaming que te interese?",
  "Mi conocimiento se centra en videojuegos. Si quieres hablar de otro tema, puedo intentar relacionarlo con el mundo de los videojuegos si es posible.",
  "Estoy especializado en conversar sobre videojuegos. ¿Quieres que hablemos sobre algún juego, consola o tendencia reciente en la industria?"
];

/**
 * Determina si un texto está relacionado con videojuegos
 * @param text - El texto a analizar
 * @returns boolean - Verdadero si está relacionado con videojuegos
 */
export function is_gaming_related(text: string): boolean {
  const lowerText = text.toLowerCase();
  
  // Verificar si contiene palabras clave de videojuegos
  const allGamingTerms = [
    ...GAMING_VOCABULARY.generos,
    ...GAMING_VOCABULARY.plataformas,
    ...GAMING_VOCABULARY.terminos_tecnicos,
    ...GAMING_VOCABULARY.companias,
    ...GAMING_VOCABULARY.eventos,
    'juego', 'videojuego', 'consola', 'gaming', 'gamer', 'jugador',
    'jugar', 'partida', 'nivel', 'personaje', 'mando', 'joystick'
  ];
  
  // Verificar si menciona algún juego popular
  const popularGameTitles = Object.keys(POPULAR_GAMES);
  
  // Comprobar si el texto contiene términos de videojuegos
  for (const term of allGamingTerms) {
    if (lowerText.includes(term)) {
      return true;
    }
  }
  
  // Comprobar si el texto menciona algún juego popular
  for (const game of popularGameTitles) {
    if (lowerText.includes(game)) {
      return true;
    }
  }
  
  return false;
}

/**
 * Genera una respuesta relacionada con videojuegos basada en el texto del usuario
 * @param userText - El texto del usuario
 * @returns string - Respuesta generada
 */
export function get_gaming_response(userText: string): string {
  const lowerText = userText.toLowerCase();
  
  // Si no está relacionado con videojuegos, redirigir la conversación
  if (!is_gaming_related(userText)) {
    return OFF_TOPIC_RESPONSES[Math.floor(Math.random() * OFF_TOPIC_RESPONSES.length)];
  }
  
  // Verificar si menciona algún juego específico
  for (const [game, info] of Object.entries(POPULAR_GAMES)) {
    if (lowerText.includes(game)) {
      return `¡${game.charAt(0).toUpperCase() + game.slice(1)} es un gran juego! ${info.descripcion} Fue desarrollado por ${info.desarrollador} y está disponible en ${info.plataformas.join(', ')}. ¿Has jugado a otros juegos de ${info.genero}?`;
    }
  }
  
  // Verificar si menciona algún género
  for (const genero of GAMING_VOCABULARY.generos) {
    if (lowerText.includes(genero)) {
      return `Los juegos de ${genero} son fascinantes. ¿Tienes algún título favorito de este género? Hay muchas opciones interesantes para explorar.`;
    }
  }
  
  // Verificar si menciona alguna plataforma
  for (const plataforma of GAMING_VOCABULARY.plataformas) {
    if (lowerText.includes(plataforma)) {
      return `${plataforma.charAt(0).toUpperCase() + plataforma.slice(1)} es una gran plataforma para jugar. ¿Qué juegos has probado en ella? Hay muchos títulos exclusivos y multiplataforma disponibles.`;
    }
  }
  
  // Verificar si menciona alguna compañía
  for (const compania of GAMING_VOCABULARY.companias) {
    if (lowerText.includes(compania)) {
      return `${compania.charAt(0).toUpperCase() + compania.slice(1)} ha desarrollado algunos juegos increíbles. ¿Tienes algún título favorito de esta compañía? Han contribuido significativamente a la industria.`;
    }
  }
  
  // Si no hay coincidencias específicas, devolver una respuesta general sobre videojuegos
  return GAMING_RESPONSES[Math.floor(Math.random() * GAMING_RESPONSES.length)];
}

/**
 * Analiza el contenido relacionado con videojuegos en un texto
 * @param text - El texto a analizar
 * @returns Objeto con análisis de contenido gaming
 */
export function analyze_gaming_content(text: string) {
  const lowerText = text.toLowerCase();
  const result = {
    is_gaming_related: is_gaming_related(text),
    keywords: [] as Array<{word: string, category: string}>,
    games_mentioned: [] as string[],
    categories: {} as Record<string, number>
  };
  
  // Buscar juegos mencionados
  for (const game of Object.keys(POPULAR_GAMES)) {
    if (lowerText.includes(game)) {
      result.games_mentioned.push(game.charAt(0).toUpperCase() + game.slice(1));
    }
  }
  
  // Categorizar palabras clave encontradas
  const categories = [
    {name: 'género', terms: GAMING_VOCABULARY.generos},
    {name: 'plataforma', terms: GAMING_VOCABULARY.plataformas},
    {name: 'técnico', terms: GAMING_VOCABULARY.terminos_tecnicos},
    {name: 'compañía', terms: GAMING_VOCABULARY.companias},
    {name: 'evento', terms: GAMING_VOCABULARY.eventos}
  ];
  
  // Contar categorías y palabras clave
  for (const category of categories) {
    let count = 0;
    for (const term of category.terms) {
      if (lowerText.includes(term)) {
        result.keywords.push({word: term, category: category.name});
        count++;
      }
    }
    if (count > 0) {
      result.categories[category.name] = count;
    }
  }
  
  return result;
}