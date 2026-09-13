import { Emotion } from "../types";

interface EmotionBadgeProps {
  emotions: Emotion[];
}

export function EmotionBadge({ emotions }: EmotionBadgeProps) {
  if (!emotions || emotions.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2 mt-2">
      {emotions.map((item, index) => {
        const percentage = Math.round(item.confidence * 100);
        return (
          <span
            key={index}
            className="inline-flex items-center gap-1.5 px-3 py-1 bg-slate-100 border border-slate-200 rounded-full text-xs font-medium text-slate-700"
          >
            <span>{item.emotion}</span>
            <span className="bg-slate-200 text-slate-800 text-[10px] font-bold px-1.5 py-0.5 rounded-full">
              {percentage}%
            </span>
          </span>
        );
      })}
    </div>
  );
}
