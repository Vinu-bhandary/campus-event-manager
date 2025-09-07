import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function LogoutButton() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const handleLogout = async () => {
    try {
      await axios.post("http://127.0.0.1:8000/api/logout/", null, {
        params: { token },
      });
    } catch (err) {
      console.error("Logout error:", err);
    }
    // Clear local storage
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("user_id");

    // Redirect to login
    navigate("/");
  };

  return (
    <button
      onClick={handleLogout}
      className="bg-red-500 text-white px-3 py-1 rounded ml-4"
    >
      Logout
    </button>
  );
}
