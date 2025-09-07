// src/App.jsx
import { useState } from "react"
import axios from "axios"
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet"
import "leaflet/dist/leaflet.css"

export default function App() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState([])

  const handleSearch = async () => {
    if (!query) return
    try {
      const res = await axios.post("http://localhost:8000/search", { query })
      console.log("API Response:", res.data) 
      setResults(res.data)
    } catch (err) {
      console.error("Search error:", err)
    }
  }

  return (
    <div className="min-h-screen bg-sky-50 p-6">
      <h1 className="text-3xl font-bold text-center mb-6">
        🌊 FloatChat Explorer — Ask the Ocean
      </h1>

      {/* Query Box */}
      <div className="flex justify-center mb-6">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Find warm, salty water in the Indian Ocean"
          className="w-2/3 p-3 border rounded-l-xl focus:outline-none"
        />
        <button
          onClick={handleSearch}
          className="bg-blue-600 text-white px-4 py-2 rounded-r-xl hover:bg-blue-700"
        >
          🔍 Search
        </button>
      </div>

      {/* Results Table */}
      {results.length > 0 && (
        <div className="overflow-x-auto mb-8">
          <table className="table-auto border-collapse border border-gray-400 w-full">
            <thead className="bg-blue-100">
              <tr>
                <th className="border border-gray-400 px-4 py-2">Date</th>
                <th className="border border-gray-400 px-4 py-2">Latitude</th>
                <th className="border border-gray-400 px-4 py-2">Longitude</th>
                <th className="border border-gray-400 px-4 py-2">Temp (°C)</th>
                <th className="border border-gray-400 px-4 py-2">Salinity</th>
                <th className="border border-gray-400 px-4 py-2">Score</th>
              </tr>
            </thead>
            <tbody>
              {results.map((row, i) => (
                <tr key={i} className="hover:bg-gray-100">
                  <td className="border border-gray-400 px-4 py-2">{row.date_time}</td>
                  <td className="border border-gray-400 px-4 py-2">{row.latitude}</td>
                  <td className="border border-gray-400 px-4 py-2">{row.longitude}</td>
                  <td className="border border-gray-400 px-4 py-2">{row.temperature_mean.toFixed(2)}</td>
                  <td className="border border-gray-400 px-4 py-2">{row.salinity_mean.toFixed(2)}</td>
                  <td className="border border-gray-400 px-4 py-2">{row.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Map View */}
      {results.length > 0 && (
        <div className="h-[500px] w-full rounded-xl shadow-lg">
          <MapContainer
            center={[results[0].latitude, results[0].longitude]}
            zoom={3}
            style={{ height: "100%", width: "100%" }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {results.map((row, i) => (
              <CircleMarker
                key={i}
                center={[row.latitude, row.longitude]}
                radius={6}
                pathOptions={{ color: "blue", fillColor: "cyan" }}
              >
                <Popup>
                  <div>
                    <strong>Date:</strong> {row.date_time} <br />
                    <strong>Temp:</strong> {row.temperature_mean.toFixed(2)} <br />
                    <strong>Salinity:</strong> {row.salinity_mean.toFixed(2)}
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        </div>
      )}
    </div>
  )
}
