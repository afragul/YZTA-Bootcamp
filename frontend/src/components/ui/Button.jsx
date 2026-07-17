// Ortak buton bileşeni.
// Kullanım: <Button>Kaydet</Button>  |  <Button variant="secondary">İptal</Button>
//          <Button variant="ghost">Geri</Button>

const base =
  "inline-flex items-center justify-center gap-2 rounded-lg px-5 py-2.5 " +
  "text-sm font-semibold transition-colors disabled:opacity-50 " +
  "disabled:cursor-not-allowed focus-visible:outline-none";

const variants = {
  // Ana aksiyon — koyu mavi
  primary: "bg-primary-800 text-primary-50 hover:bg-primary-950",
  // İkincil — çerçeveli
  secondary:
    "border border-primary-200 bg-white text-primary-800 hover:bg-primary-50",
  // Sade — arka planı yok
  ghost: "text-primary-500 hover:bg-primary-50",
};

export default function Button({
  variant = "primary",
  className = "",
  ...props
}) {
  return (
    <button
      className={`${base} ${variants[variant]} ${className}`}
      {...props}
    />
  );
}
