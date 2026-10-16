"use client";
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { Activity, ShieldAlert, ArrowRight, CheckCircle2, FlaskConical, TrendingUp } from 'lucide-react';

const funnelData = [
  { name: 'Captured', count: 124 },
  { name: 'Extracting', count: 86 },
  { name: 'Validated', count: 42 },
  { name: 'Backtesting', count: 28 },
  { name: 'Approved', count: 12 },
  { name: 'Deployed', count: 5 },
];

const portfolioData = [
  { month: 'Jan', value: 100000 },
  { month: 'Feb', value: 105000 },
  { month: 'Mar', value: 103000 },
  { month: 'Apr', value: 112000 },
  { month: 'May', value: 118000 },
  { month: 'Jun', value: 125000 },
];

export default function Dashboard() {
  const [strategies, setStrategies] = useState<any[]>([]);

  useEffect(() => {
    // Fetch mock data or real data from the API
    fetch('http://localhost:8000/strategies/')
      .then(res => res.json())
      .then(data => setStrategies(data))
      .catch(err => {
        console.error("Could not fetch strategies, using mock data", err);
        setStrategies([
          { id: 1, name: "Mean Reversion Nifty50", lifecycle_state: "BACKTESTING", updated_at: new Date().toISOString() },
          { id: 2, name: "Momentum Breakout Midcap", lifecycle_state: "IDEA_CAPTURED", updated_at: new Date().toISOString() },
          { id: 3, name: "Options Straddle Earnings", lifecycle_state: "DEPLOYED_EXTERNALLY", updated_at: new Date().toISOString() },
        ]);
      });
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 p-8 text-slate-900">
      <header className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Quant Research Brain</h1>
          <p className="text-slate-500">Unified Control Center</p>
        </div>
        <div className="flex gap-4">
          <button className="px-4 py-2 bg-white border border-slate-200 rounded-md shadow-sm hover:bg-slate-50 font-medium">
            New Source
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700 font-medium flex items-center gap-2">
            <Activity size={18} /> Run Validation
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">

        {/* Strategy Funnel */}
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <FlaskConical className="text-blue-500" /> Strategy Funnel
            </h2>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnelData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={100} />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="space-y-4">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="p-3 bg-green-100 text-green-600 rounded-lg">
              <CheckCircle2 size={24} />
            </div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Passed Validation</p>
              <p className="text-2xl font-bold">42</p>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="p-3 bg-red-100 text-red-600 rounded-lg">
              <ShieldAlert size={24} />
            </div>
            <div>
              <p className="text-sm text-slate-500 font-medium">High Bias Risk</p>
              <p className="text-2xl font-bold">7</p>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="p-3 bg-purple-100 text-purple-600 rounded-lg">
              <TrendingUp size={24} />
            </div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Deployed Capital</p>
              <p className="text-2xl font-bold">₹1.2Cr</p>
            </div>
          </div>
        </div>

      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

        {/* Strategy Registry */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Active Strategies</h2>
            <Link href="/strategies" className="text-sm text-blue-600 hover:underline flex items-center gap-1">
              View all <ArrowRight size={14} />
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="py-3 px-4 font-medium text-slate-500">Name</th>
                  <th className="py-3 px-4 font-medium text-slate-500">Status</th>
                  <th className="py-3 px-4 font-medium text-slate-500 text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {strategies.map((strategy) => (
                  <tr key={strategy.id} className="border-b border-slate-100 hover:bg-slate-50">
                    <td className="py-3 px-4 font-medium">{strategy.name}</td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">
                        {strategy.lifecycle_state}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <Link href={`/strategy/${strategy.id}`} className="text-blue-600 hover:underline text-sm font-medium">
                        Analyze
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Portfolio Overview */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <TrendingUp className="text-green-500" /> Portfolio Simulation
          </h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={portfolioData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}
