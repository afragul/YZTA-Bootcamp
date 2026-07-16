import { NavLink, Outlet } from "react-router-dom";

// Tüm sayfaları saran ortak kabuk: üst menü + içerik alanı.
// <Outlet /> = o an aktif olan sayfanın gösterildiği yer.

const links = [
  { to: "/upload", label: "CV Yükle" },
  { to: "/dashboard", label: "Panel" },
  { to: "/chat", label: "AI Koç" },
];

export default function Layout() {
  return (
    <div className="min-h-screen">
      <header className="border-b border-primary-200 bg-white">
        <nav className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <NavLink to="/" className="text-lg font-bold text-primary-800">
            NextGenCV
          </NavLink>

          <div className="flex items-center gap-1">
            {links.map((l) => (
              <NavLink
                key={l.to}
                to={l.to}
                className={({ isActive }) =>
                  "rounded-lg px-3 py-2 text-sm font-medium transition-colors " +
                  (isActive
                    ? "bg-primary-50 text-primary-800"
                    : "text-muted hover:bg-primary-50 hover:text-primary-800")
                }
              >
                {l.label}
              </NavLink>
            ))}
          </div>
        </nav>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-10">
        <Outlet />
      </main>
    </div>
  );
}
