import { createContext, useContext, useState } from "react";

// Yüklenen CV'nin analiz cevabını (CVUploadResponse) uygulama genelinde tutar.
// Upload ekranı setResult ile yazar, Dashboard useCv ile okur.
// sessionStorage ile kalıcı: Dashboard'da sayfa yenilense de veri kaybolmaz.

const STORAGE_KEY = "cv_result";
const CvContext = createContext(null);

function readInitial() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function CvProvider({ children }) {
  const [result, setResultState] = useState(readInitial);

  function setResult(next) {
    setResultState(next);
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      // storage kotası/erişimi yoksa yut — bellek-içi state yeterli
    }
  }

  function clear() {
    setResultState(null);
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch {
      // yut
    }
  }

  return (
    <CvContext.Provider value={{ result, setResult, clear }}>
      {children}
    </CvContext.Provider>
  );
}

export function useCv() {
  const ctx = useContext(CvContext);
  if (!ctx) {
    throw new Error("useCv, <CvProvider> içinde kullanılmalıdır.");
  }
  return ctx;
}
