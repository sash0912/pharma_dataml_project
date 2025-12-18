"use client";

import { useEffect, useState } from "react";

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/analytics/summary")
      .then((res) => res.json())
      .then((data) => setSummary(data));
  }, []);

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-6">
        Pharma Demand Forecast Dashboard
      </h1>

      {!summary ? (
        <p>Loading analytics...</p>
      ) : (
        <div className="grid grid-cols-4 gap-4">
          <Card title="Total Forecasts" value={summary.total_predictions} />
          <Card title="Avg Demand" value={summary.average_demand} />
          <Card title="Min Demand" value={summary.min_demand} />
          <Card title="Max Demand" value={summary.max_demand} />
        </div>
      )}
    </main>
  );
}

function Card({ title, value }: { title: string; value: number }) {
  return (
    <div className="rounded-xl bg-white shadow p-4 rounded-xl">
      <h2 className="text-gray-500 text-sm">{title}</h2>
      <p className="text-2xl font-semibold">{value}</p>
    </div>
  );
}
