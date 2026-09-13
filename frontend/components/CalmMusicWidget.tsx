"use client";

import { useState, useRef, useEffect } from "react";

interface Track {
  id: string;
  title: string;
  category: string;
  icon: string;
  url: string;
}

const NATIVE_TRACKS: Track[] = [
  {
    id: "lofi-piano",
    title: "Piano Tranquilo & Lofi",
    category: "Melodía Calma",
    icon: "🎹",
    url: "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3",
  },
  {
    id: "soft-rain",
    title: "Lluvia Suave y Bosque",
    category: "Naturaleza",
    icon: "🌧️",
    url: "https://cdn.pixabay.com/download/audio/2021/09/06/audio_946b1a329d.mp3?filename=soft-rain-ambient-111154.mp3",
  },
  {
    id: "ambient-waves",
    title: "Olas y Brisa Marina",
    category: "Relajación",
    icon: "🌊",
    url: "https://cdn.pixabay.com/download/audio/2022/03/10/audio_c8c8a73229.mp3?filename=ocean-waves-ambient-10271.mp3",
  },
  {
    id: "zen-meditation",
    title: "Frecuencia 432Hz Zen",
    category: "Meditación",
    icon: "🧘",
    url: "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=meditation-ambient-frequency-18241.mp3",
  },
];

const SPOTIFY_PRESETS = [
  { name: "Lofi Beats", id: "37i9dQZF1DX8Ueb1gM822r" },
  { name: "Peaceful Piano", id: "37i9dQZF1DX4sWSpwq3LiO" },
  { name: "Ambient Relaxation", id: "37i9dQZF1DWZQD1JICOwBx" },
  { name: "Deep Focus", id: "37i9dQZF1DWZeKCadgRdKQ" }
];

const YOUTUBE_PRESETS = [
  { name: "Lofi Girl 24/7 Live", videoId: "jfKfPfyJRdk" },
  { name: "Lofi Hip Hop Radio", videoId: "5qap5aO4i9A" },
  { name: "Lluvia & Piano Relajante", videoId: "lP26UCnoHya" },
  { name: "Música Mariachi Tranquila", videoId: "hTWKbfoikeg" }
];

export function CalmMusicWidget() {
  const [isMinimized, setIsMinimized] = useState(true);
  const [activeTab, setActiveTab] = useState<"native" | "spotify" | "youtube">("native");
  
  // Estado Nativo
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTrackIndex, setCurrentTrackIndex] = useState(0);
  const [volume, setVolume] = useState(0.5);
  const [isMuted, setIsMuted] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Estado Spotify
  const [selectedSpotifyId, setSelectedSpotifyId] = useState(SPOTIFY_PRESETS[0].id);
  const [customSpotifyInput, setCustomSpotifyInput] = useState("");

  // Estado YouTube
  const [selectedYoutubeId, setSelectedYoutubeId] = useState(YOUTUBE_PRESETS[0].videoId);
  const [customYoutubeInput, setCustomYoutubeInput] = useState("");

  const currentTrack = NATIVE_TRACKS[currentTrackIndex];

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = isMuted ? 0 : volume;
    }
  }, [volume, isMuted]);

  const toggleNativePlay = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current
        .play()
        .then(() => setIsPlaying(true))
        .catch((err) => console.log("Audio play blocked by browser policy:", err));
    }
  };

  const handleSelectNativeTrack = (index: number) => {
    setCurrentTrackIndex(index);
    setIsPlaying(false);
    setTimeout(() => {
      if (audioRef.current) {
        audioRef.current.play().then(() => setIsPlaying(true)).catch(() => {});
      }
    }, 100);
  };

  const handleCustomSpotifySubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customSpotifyInput) return;
    let match = customSpotifyInput.match(/(?:playlist|track|album)\/([a-zA-Z0-9]+)/);
    if (match && match[1]) {
      setSelectedSpotifyId(match[1]);
    } else {
      setSelectedSpotifyId(customSpotifyInput.trim());
    }
  };

  const handleCustomYoutubeSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customYoutubeInput) return;
    let match = customYoutubeInput.match(/(?:v=|\/live\/|youtu\.be\/|\/embed\/)([a-zA-Z0-9_-]{11})/);
    if (match && match[1]) {
      setSelectedYoutubeId(match[1]);
    } else if (customYoutubeInput.length === 11) {
      setSelectedYoutubeId(customYoutubeInput.trim());
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      <audio
        ref={audioRef}
        src={currentTrack.url}
        loop
        onEnded={() => setIsPlaying(false)}
      />

      {/* Contenedor Principal: Se mantiene siempre en el DOM para NO pausar la música al minimizar */}
      <div
        className={`bg-slate-900/95 text-white backdrop-blur-xl border border-white/20 rounded-2xl shadow-2xl transition-all duration-300 overflow-hidden ${
          isMinimized
            ? "w-72 p-3 space-y-2"
            : "w-88 sm:w-96 p-5 space-y-4"
        }`}
      >
        {/* Encabezado del Widget */}
        <div className="flex items-center justify-between border-b border-white/10 pb-2.5">
          <div className="flex items-center gap-2">
            <span className="text-lg">🎵</span>
            <div>
              <h4 className="text-xs font-bold text-white leading-tight">Música Tranquila</h4>
              {!isMinimized && (
                <p className="text-[10px] text-emerald-400 font-medium">Spotify, YouTube & Nativo</p>
              )}
            </div>
          </div>
          <button
            onClick={() => setIsMinimized(!isMinimized)}
            className="text-slate-300 hover:text-white text-xs font-bold px-2 py-1 rounded-md bg-white/10 hover:bg-white/20 transition-colors cursor-pointer"
          >
            {isMinimized ? "🔍 Ampliar" : "🗕 Reducir"}
          </button>
        </div>

        {/* MODO MINIMIZADO COMPACTO (El iframe NO se destruye, solo se hace compacto) */}
        {isMinimized && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-[11px] text-emerald-400 font-semibold truncate">
                Modo: {activeTab === "native" ? "🌿 Nativo" : activeTab === "spotify" ? "🟢 Spotify" : "▶️ YouTube"}
              </span>
              {activeTab === "native" && (
                <button
                  onClick={toggleNativePlay}
                  className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-white font-bold text-xs"
                >
                  {isPlaying ? "⏸ Pausa" : "▶ Play"}
                </button>
              )}
            </div>

            {/* Vista Compacta de iframe para Spotify/YouTube */}
            {activeTab === "spotify" && (
              <div className="h-20 overflow-hidden rounded-lg border border-white/10">
                <iframe
                  src={`https://open.spotify.com/embed/playlist/${selectedSpotifyId}?utm_source=generator&theme=0`}
                  width="100%"
                  height="80"
                  frameBorder="0"
                  allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                  loading="lazy"
                />
              </div>
            )}

            {activeTab === "youtube" && (
              <div className="h-24 overflow-hidden rounded-lg border border-white/10 bg-black">
                <iframe
                  width="100%"
                  height="96"
                  src={`https://www.youtube.com/embed/${selectedYoutubeId}?autoplay=1`}
                  title="YouTube Player"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowFullScreen
                />
              </div>
            )}
          </div>
        )}

        {/* MODO EXPANDIDO COMPLETO */}
        {!isMinimized && (
          <div className="space-y-4">
            {/* Selector de Pestañas (Nativo, Spotify, YouTube) */}
            <div className="flex bg-white/10 p-1 rounded-xl gap-1 text-xs">
              <button
                onClick={() => setActiveTab("native")}
                className={`flex-1 py-1.5 rounded-lg font-semibold transition-all cursor-pointer ${
                  activeTab === "native" ? "bg-emerald-600 text-white shadow-sm" : "text-slate-300 hover:text-white"
                }`}
              >
                🌿 Nativo
              </button>
              <button
                onClick={() => {
                  if (isPlaying && audioRef.current) {
                    audioRef.current.pause();
                    setIsPlaying(false);
                  }
                  setActiveTab("spotify");
                }}
                className={`flex-1 py-1.5 rounded-lg font-semibold transition-all cursor-pointer ${
                  activeTab === "spotify" ? "bg-emerald-600 text-white shadow-sm" : "text-slate-300 hover:text-white"
                }`}
              >
                🟢 Spotify
              </button>
              <button
                onClick={() => {
                  if (isPlaying && audioRef.current) {
                    audioRef.current.pause();
                    setIsPlaying(false);
                  }
                  setActiveTab("youtube");
                }}
                className={`flex-1 py-1.5 rounded-lg font-semibold transition-all cursor-pointer ${
                  activeTab === "youtube" ? "bg-emerald-600 text-white shadow-sm" : "text-slate-300 hover:text-white"
                }`}
              >
                ▶️ YouTube
              </button>
            </div>

            {/* Pestaña Nativa */}
            {activeTab === "native" && (
              <div className="space-y-3">
                <div className="bg-white/5 p-3.5 rounded-xl border border-white/10 space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2.5 overflow-hidden">
                      <span className="text-2xl p-2 bg-emerald-950/80 border border-emerald-500/40 rounded-xl">
                        {currentTrack.icon}
                      </span>
                      <div className="truncate">
                        <span className="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">
                          {currentTrack.category}
                        </span>
                        <h5 className="text-xs font-semibold text-white truncate">{currentTrack.title}</h5>
                      </div>
                    </div>

                    <button
                      onClick={toggleNativePlay}
                      className="w-10 h-10 bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white rounded-full flex items-center justify-center shadow-lg transition-transform text-lg cursor-pointer flex-shrink-0"
                    >
                      {isPlaying ? "⏸" : "▶"}
                    </button>
                  </div>

                  {isPlaying && (
                    <div className="flex items-center justify-center gap-1 h-3 pt-1">
                      <span className="w-1 bg-emerald-400 h-full animate-bounce rounded-full" />
                      <span className="w-1 bg-emerald-400 h-2/3 animate-bounce delay-75 rounded-full" />
                      <span className="w-1 bg-emerald-400 h-full animate-bounce delay-150 rounded-full" />
                      <span className="w-1 bg-emerald-400 h-1/2 animate-bounce delay-100 rounded-full" />
                    </div>
                  )}
                </div>

                <div className="space-y-1 max-h-32 overflow-y-auto pr-1 custom-scrollbar">
                  {NATIVE_TRACKS.map((track, idx) => (
                    <button
                      key={track.id}
                      onClick={() => handleSelectNativeTrack(idx)}
                      className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium flex items-center justify-between transition-colors cursor-pointer ${
                        currentTrackIndex === idx
                          ? "bg-emerald-600/30 text-emerald-300 border border-emerald-500/40"
                          : "bg-white/5 text-slate-300 hover:bg-white/10"
                      }`}
                    >
                      <span className="flex items-center gap-2 truncate">
                        <span>{track.icon}</span>
                        <span className="truncate">{track.title}</span>
                      </span>
                      {currentTrackIndex === idx && <span className="text-[10px] text-emerald-400">● Activo</span>}
                    </button>
                  ))}
                </div>

                <div className="flex items-center gap-3 pt-2 border-t border-white/10 text-xs">
                  <button onClick={() => setIsMuted(!isMuted)} className="text-slate-400 hover:text-white cursor-pointer">
                    {isMuted || volume === 0 ? "🔇" : "🔊"}
                  </button>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.05"
                    value={isMuted ? 0 : volume}
                    onChange={(e) => {
                      setVolume(parseFloat(e.target.value));
                      setIsMuted(false);
                    }}
                    className="w-full h-1.5 bg-slate-700 accent-emerald-500 rounded-lg cursor-pointer"
                  />
                </div>
              </div>
            )}

            {/* Pestaña Spotify */}
            {activeTab === "spotify" && (
              <div className="space-y-3">
                <div className="flex flex-wrap gap-1">
                  {SPOTIFY_PRESETS.map((sp) => (
                    <button
                      key={sp.id}
                      onClick={() => setSelectedSpotifyId(sp.id)}
                      className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition-colors cursor-pointer ${
                        selectedSpotifyId === sp.id ? "bg-emerald-600 text-white" : "bg-white/10 text-slate-300 hover:bg-white/20"
                      }`}
                    >
                      {sp.name}
                    </button>
                  ))}
                </div>

                <div className="rounded-xl overflow-hidden border border-white/10 shadow-inner">
                  <iframe
                    src={`https://open.spotify.com/embed/playlist/${selectedSpotifyId}?utm_source=generator&theme=0`}
                    width="100%"
                    height="152"
                    frameBorder="0"
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy"
                  />
                </div>

                <form onSubmit={handleCustomSpotifySubmit} className="flex gap-2 pt-1">
                  <input
                    type="text"
                    value={customSpotifyInput}
                    onChange={(e) => setCustomSpotifyInput(e.target.value)}
                    placeholder="Pegar enlace de Spotify..."
                    className="flex-1 px-3 py-1.5 bg-white/10 border border-white/20 rounded-lg text-xs text-white placeholder-slate-400 outline-none focus:border-emerald-400"
                  />
                  <button
                    type="submit"
                    className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs rounded-lg transition-colors cursor-pointer"
                  >
                    Cargar
                  </button>
                </form>
              </div>
            )}

            {/* Pestaña YouTube */}
            {activeTab === "youtube" && (
              <div className="space-y-3">
                <div className="flex flex-wrap gap-1">
                  {YOUTUBE_PRESETS.map((yt) => (
                    <button
                      key={yt.videoId}
                      onClick={() => setSelectedYoutubeId(yt.videoId)}
                      className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition-colors cursor-pointer ${
                        selectedYoutubeId === yt.videoId ? "bg-emerald-600 text-white" : "bg-white/10 text-slate-300 hover:bg-white/20"
                      }`}
                    >
                      {yt.name}
                    </button>
                  ))}
                </div>

                <div className="rounded-xl overflow-hidden border border-white/10 shadow-inner bg-black aspect-video flex items-center justify-center">
                  <iframe
                    width="100%"
                    height="180"
                    src={`https://www.youtube.com/embed/${selectedYoutubeId}?autoplay=1`}
                    title="YouTube Player"
                    frameBorder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowFullScreen
                    className="w-full h-full rounded-xl"
                  />
                </div>

                <form onSubmit={handleCustomYoutubeSubmit} className="flex gap-2 pt-1">
                  <input
                    type="text"
                    value={customYoutubeInput}
                    onChange={(e) => setCustomYoutubeInput(e.target.value)}
                    placeholder="Pegar enlace de YouTube..."
                    className="flex-1 px-3 py-1.5 bg-white/10 border border-white/20 rounded-lg text-xs text-white placeholder-slate-400 outline-none focus:border-emerald-400"
                  />
                  <button
                    type="submit"
                    className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs rounded-lg transition-colors cursor-pointer"
                  >
                    Cargar
                  </button>
                </form>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
