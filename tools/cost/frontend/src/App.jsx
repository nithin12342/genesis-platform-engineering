import { useState, useEffect } from 'react'
import axios from 'axios'
import { Activity } from 'lucide-react'

function App() {
  const [data, setData] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get('/api/status')
        setData(res.data)
      } catch (e) { console.error(e) }
    }
    fetchData()
    const interval = setInterval(fetchData, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      <h1>08 Cost Optimization Monitoring Tool</h1>
      <div className="card">
        <h3><Activity size={20} style={{verticalAlign: 'middle', marginRight: '10px'}}/> Live Status</h3>
        {!data ? <p>Loading...</p> : (
          <div>
            {Object.entries(data).map(([key, value]) => (
              <div key={key} className="metric">
                <span className="label">{key.replace(/_/g, ' ').toUpperCase()}</span>
                <span className="value">{value.toString()}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
