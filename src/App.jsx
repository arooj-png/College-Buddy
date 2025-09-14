import React, { useState, useRef, useEffect } from 'react'

export default function App() {
  const [messages, setMessages] = useState([
    { id: 1, from: 'bot', text: "Hey buddy 👋 — I'm College Buddy. Ask me about fees, hostel rules, or deadlines!" }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [mood, setMood] = useState('supportive')
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
    if (import.meta.env.MODE === 'development') {
      console.log('✅ Frontend running in dev mode')
    }
  }, [messages])

  async function send() {
    const q = input.trim()
    if (!q) return
    const user = { id: Date.now(), from: 'user', text: q }
    setMessages(m => [...m, user])
    setInput('')
    setLoading(true)
    try {
      const res = await fetch('http://127.0.0.1:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q, mood })
      })
      const data = await res.json()
      setMessages(m => [...m, { id: Date.now()+1, from: 'bot', text: data.answer }])
    } catch (e) {
      setMessages(m => [...m, { id: Date.now()+2, from: 'bot', text: "Can't reach server — run backend." }])
    } finally {
      setLoading(false)
    }
  }

  function MoodPill({ value }) {
    return (
      <button
        onClick={() => setMood(value)}
        className={`px-3 py-1 rounded-full text-sm font-medium mr-2 border ${mood===value ? 'bg-white text-gray-900 shadow' : 'bg-transparent text-white/90 border-white/30'}`}>
        {value}
      </button>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white/90 rounded-2xl shadow-2xl overflow-hidden">
        <header className="px-5 py-4 bg-gradient-to-r from-indigo-600 to-violet-600 text-white flex items-center justify-between">
          <div>
            <h1 className="text-lg font-bold">🎓 College Buddy</h1>
            <p className="text-xs opacity-90">Friendly campus FAQ — like a helpful senior</p>
          </div>
          <img src="https://api.dicebear.com/6.x/thumbs/svg?seed=college-buddy" alt="avatar" className="w-10 h-10 rounded-full" />
        </header>

        <main className="px-4 py-3 h-[60vh] overflow-y-auto bg-gradient-to-b from-white/0 to-white/5">
          {messages.map(m => (
            <div key={m.id} className={`mb-3 flex ${m.from==='user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`${m.from==='user' ? 'bg-indigo-600 text-white rounded-tl-2xl rounded-bl-2xl rounded-tr-md px-4 py-2' : 'bg-white/95 text-gray-900 rounded-tr-2xl rounded-br-2xl rounded-tl-md px-4 py-2 shadow'}`}>
                <div className="text-sm leading-relaxed">{m.text}</div>
              </div>
            </div>
          ))}
          <div ref={endRef} />
        </main>

        <footer className="px-4 py-3 bg-transparent">
          <div className="mb-2 flex items-center px-1">
            <div className="text-xs text-gray-600 mr-2">Tone:</div>
            <MoodPill value='supportive' />
            <MoodPill value='casual' />
            <MoodPill value='professional' />
          </div>
          <div className="flex items-center p-1">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key==='Enter') send() }}
              placeholder="Ask: When is the fee deadline?"
              className="flex-1 rounded-full px-4 py-2 mr-3 border border-gray-200 outline-none"
            />
            <button onClick={send} className={`px-4 py-2 rounded-full ${loading ? 'bg-gray-300 text-gray-600' : 'bg-indigo-600 text-white'}`}>{loading ? '…' : 'Send'}</button>
          </div>
        </footer>
      </div>
    </div>
  )
}
