import { Recommendation } from "../types";

interface RecommendationCardProps {
  recommendations: Recommendation[];
}

export function RecommendationCard({ recommendations }: RecommendationCardProps) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="space-y-4 mt-4">
      <h4 className="text-base font-bold text-slate-900 border-b border-slate-200 pb-2">
        Alternativas de Actuación Sugeridas
      </h4>
      <div className="grid gap-4 md:grid-cols-2">
        {recommendations.map((rec, index) => (
          <div
            key={index}
            className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <h5 className="font-bold text-slate-900 text-sm">{rec.title}</h5>
                <span className="text-[10px] uppercase font-bold tracking-wider bg-blue-50 text-blue-700 px-2 py-0.5 rounded border border-blue-200">
                  Opción #{rec.priority}
                </span>
              </div>
              <p className="text-xs text-slate-600 mb-4 leading-relaxed">{rec.description}</p>
            </div>

            <div className="space-y-2 text-xs pt-3 border-t border-slate-100">
              {rec.benefit && (
                <div className="bg-emerald-50 text-emerald-800 p-2.5 rounded-lg border border-emerald-200/60">
                  <strong className="block text-emerald-900 mb-0.5">Beneficio:</strong>
                  {rec.benefit}
                </div>
              )}
              {rec.risk && (
                <div className="bg-amber-50 text-amber-800 p-2.5 rounded-lg border border-amber-200/60">
                  <strong className="block text-amber-900 mb-0.5">Posible riesgo:</strong>
                  {rec.risk}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
