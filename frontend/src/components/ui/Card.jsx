// Ortak kart bileşeni — içerik gruplamak için.
// Kullanım:
//   <Card>
//     <Card.Title>Başlık</Card.Title>
//     <p>...</p>
//   </Card>

export default function Card({ className = "", ...props }) {
  return (
    <div
      className={
        "rounded-2xl border border-primary-200 bg-white p-6 " +
        "shadow-sm " +
        className
      }
      {...props}
    />
  );
}

Card.Title = function CardTitle({ className = "", ...props }) {
  return (
    <h3
      className={"mb-2 text-lg font-semibold text-primary-800 " + className}
      {...props}
    />
  );
};
