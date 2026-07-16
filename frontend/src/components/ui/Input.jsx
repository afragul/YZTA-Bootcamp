// Ortak input bileşeni (etiketli).
// Kullanım:
//   <Input label="E-posta" type="email" value={mail} onChange={...} />

export default function Input({ label, id, className = "", ...props }) {
  const inputId = id || props.name;
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label
          htmlFor={inputId}
          className="text-sm font-medium text-primary-800"
        >
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={
          "rounded-lg border border-primary-200 bg-white px-3.5 py-2.5 " +
          "text-sm text-primary-950 placeholder:text-muted " +
          "focus-visible:border-primary-500 focus-visible:outline-none " +
          className
        }
        {...props}
      />
    </div>
  );
}
