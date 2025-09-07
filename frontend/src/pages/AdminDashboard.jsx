import { useEffect, useState } from "react";
import axios from "axios";
import LogoutButton from "../components/LogoutButton";

export default function AdminDashboard() {
  const token = localStorage.getItem("token");
  const [events, setEvents] = useState([]);
  const [title, setTitle] = useState("");
  const [type, setType] = useState("workshop");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [location, setLocation] = useState("");
  const [capacity, setCapacity] = useState("");
  const [popularity, setPopularity] = useState([]);
  const [participation, setParticipation] = useState([]);

  // Fetch events
  const fetchEvents = async () => {
    const res = await axios.get("http://127.0.0.1:8000/api/events/", {
      params: { token },
    });
    setEvents(res.data);
  };

  // Fetch reports
  const fetchReports = async () => {
    const pop = await axios.get("http://127.0.0.1:8000/api/reports/event-popularity/", {
      params: { token },
    });
    setPopularity(pop.data);

    const part = await axios.get("http://127.0.0.1:8000/api/reports/student-participation/", {
      params: { token },
    });
    setParticipation(part.data);
  };

  useEffect(() => {
    fetchEvents();
    fetchReports();
  }, []);

  // Create event
  const handleCreate = async (e) => {
    e.preventDefault();
    await axios.post("http://127.0.0.1:8000/api/events/", {
      title,
      description: "",
      type,
      start_datetime: start,
      end_datetime: end,
      location,
      capacity: capacity ? parseInt(capacity) : null,
    }, { params: { token } });

    setTitle(""); setStart(""); setEnd(""); setLocation(""); setCapacity("");
    fetchEvents();
    fetchReports();
  };

  return (
    <div className="p-6">
        <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold mb-6 flex justify-between items-center">
            Admin Dashboard
            <LogoutButton />
            </h1>
        </div>


      {/* Event Creation */}
      <div className="bg-white p-4 shadow rounded mb-6">
        <h2 className="text-lg font-semibold mb-2">Create Event</h2>
        <form onSubmit={handleCreate} className="grid grid-cols-2 gap-4">
          <input className="border p-2" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
          <select className="border p-2" value={type} onChange={(e) => setType(e.target.value)}>
            <option value="workshop">Workshop</option>
            <option value="fest">Fest</option>
            <option value="seminar">Seminar</option>
            <option value="talk">Talk</option>
            <option value="other">Other</option>
          </select>
          <input className="border p-2" type="datetime-local" value={start} onChange={(e) => setStart(e.target.value)} required />
          <input className="border p-2" type="datetime-local" value={end} onChange={(e) => setEnd(e.target.value)} required />
          <input className="border p-2 col-span-2" placeholder="Location" value={location} onChange={(e) => setLocation(e.target.value)} />
          <input className="border p-2 col-span-2" type="number" placeholder="Capacity" value={capacity} onChange={(e) => setCapacity(e.target.value)} />
          <button type="submit" className="bg-blue-500 text-white py-2 rounded col-span-2">Create Event</button>
        </form>
      </div>

      {/* Events List */}
      <div className="bg-white p-4 shadow rounded mb-6">
        <h2 className="text-lg font-semibold mb-2">Events</h2>
        <ul className="space-y-2">
          {events.map((e) => (
            <li key={e.id} className="border p-2 rounded">
              <strong>{e.title}</strong> — {e.type} ({new Date(e.start_datetime).toLocaleString()})
            </li>
          ))}
        </ul>
      </div>

      {/* Reports */}
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white p-4 shadow rounded">
          <h2 className="text-lg font-semibold mb-2">Event Popularity</h2>
          <ul>
            {popularity.map((p, i) => (
              <li key={i}>{p.event} — {p.registrations} registrations</li>
            ))}
          </ul>
        </div>
        <div className="bg-white p-4 shadow rounded">
          <h2 className="text-lg font-semibold mb-2">Student Participation</h2>
          <ul>
            {participation.map((p, i) => (
              <li key={i}>{p.student} — attended {p.attended} events</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
