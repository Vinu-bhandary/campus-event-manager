import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children, role }) {
  const token = localStorage.getItem("token");
  const userRole = localStorage.getItem("role");

  if (!token) {
    // Not logged in → go back to login
    return <Navigate to="/" replace />;
  }

  if (role && userRole !== role) {
    // Wrong role → go back to login
    return <Navigate to="/" replace />;
  }

  return children;
}
