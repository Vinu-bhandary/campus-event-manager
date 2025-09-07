import { useEffect, useState } from "react";
import axios from "axios";
import LogoutButton from "../components/LogoutButton";

export default function StudentDashboard() {
  const token = localStorage.getItem("token");
  const [events, setEvents] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [feedbackText, setFeedbackText] = useState("");
  const [feedbackRating, setFeedbackRating] = useState(5);

  // Fetch all events
  const fetchEvents = async () => {
    const res = await axios.get("http://127.0.0.1:8000/api/events/", {
      params: { token },
    });
    setEvents(res.data);
  };

  // Fetch my registrations
  const fetchMyRegistrations = async () => {
    const res = await axios.get("http://127.0.0.1:8000/api/my-registrations/", {
      params: { token },
    });
    setRegistrations(res.data);
  };

  useEffect(() => {
    fetchEvents();
    fetchMyRegistrations();
  }, []);

  // Register for event
  const registerEvent = async (eventId) => {
    await axios.post(
      "http://127.0.0.1:8000/api/registrations/",
      { event_id: eventId },
      { params: { token } }
    );
    fetchMyRegistrations();
    alert("Registered successfully!");
  };

  // Submit feedback
  const submitFeedback = async (registrationId) => {
    await axios.post(
      "http://127.0.0.1:8000/api/feedback/",
      {
        registration_id: registrationId,
        rating: feedbackRating,
        comment: feedbackText,
      },
      { params: { token } }
    );
    setFeedbackText("");
    setFeedbackRating(5);
    alert("Feedback submitted!");
  };

  return (
    <div className="p-6">
        <div className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-bold mb-6 flex justify-between items-center">
                    Student Dashboard
                    <LogoutButton />
                    </h1>
                </div>
      {/* Events List */}
      <div className="bg-white p-4 shadow rounded mb-6">
        <h2 className="text-lg font-semibold mb-2">Available Events</h2>
        <ul className="space-y-2">
          {events.map((e) => (
            <li key={e.id} className="border p-2 rounded">
              <strong>{e.title}</strong> — {e.type} ({new Date(e.start_datetime).toLocaleString()})
              <button
                className="ml-3 bg-blue-500 text-white px-2 py-1 rounded"
                onClick={() => registerEvent(e.id)}
              >
                Register
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* My Registrations */}
      <div className="bg-white p-4 shadow rounded mb-6">
        <h2 className="text-lg font-semibold mb-2">My Registrations</h2>
        <ul className="space-y-2">
          { console.log(registrations) }
          {
          registrations.map((r, i) => (
            <li key={i} className="border p-2 rounded">
              <strong>{r.event}</strong> — Status: {r.status} — Attendance:{" "}
              {r.attendance === true
                ? "Present"
                : r.attendance === false
                ? "Absent"
                : "Not Marked"}
              <div className="mt-2">
                <textarea
                  placeholder="Leave feedback"
                  className="border p-2 w-full mb-2"
                  value={feedbackText}
                  onChange={(e) => setFeedbackText(e.target.value)}
                />
                <input
                  type="number"
                  min="1"
                  max="5"
                  className="border p-2 w-20 mr-2"
                  value={feedbackRating}
                  onChange={(e) => setFeedbackRating(e.target.value)}
                />
                <button
                  className="bg-green-500 text-white px-2 py-1 rounded"
                  onClick={() => submitFeedback(r.registration_id)}
                >
                  Submit Feedback
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
