interface SafetyAlertProps {
  warningMessage: string;
}

export function SafetyAlert({ warningMessage }: SafetyAlertProps) {
  return (
    <div className="bg-red-50 border-l-4 border-red-600 p-4 rounded-r-xl shadow-sm mb-6">
      <div className="flex items-start gap-3">
        <span className="text-2xl">⚠️</span>
        <div>
          <h3 className="text-red-900 font-bold text-base">Aviso de Seguridad de IUnderstandYou</h3>
          <p className="text-red-800 text-sm mt-1 whitespace-pre-line leading-relaxed">
            {warningMessage}
          </p>
        </div>
      </div>
    </div>
  );
}
