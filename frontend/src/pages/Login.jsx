import { useNavigate } from "react-router-dom";
import Card from "../components/ui/Card";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";

// Giriş / Kayıt ekranı — İSKELET.
// Backend bağlama (auth) Kişi 1'e ait. Burada sadece arayüz durur.

export default function Login() {
  const navigate = useNavigate();

  function handleContinue() {
    // TODO: gerçek auth çağrısı. Şimdilik panele geçir.
    navigate("/upload");
  }

  return (
    <div className="mx-auto max-w-md">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-bold text-primary-800">
          NextGenCV'ye hoş geldin
        </h1>
        <p className="mt-1 text-sm text-muted">
          CV'ni yükle, sana uygun işleri ve gelişim yolunu görelim.
        </p>
      </div>

      <Card>
        <div className="flex flex-col gap-4">
          <Input label="E-posta" name="email" type="email" placeholder="ornek@mail.com" />
          <Input label="Şifre" name="password" type="password" placeholder="••••••••" />
          <Button onClick={handleContinue}>Devam et</Button>
        </div>
      </Card>
    </div>
  );
}
