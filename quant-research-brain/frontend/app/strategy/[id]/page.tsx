"use client";
import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, CheckCircle, AlertTriangle, FileText, Database, GitMerge, LineChart, PieChart, ShieldCheck } from 'lucide-react';

export default function StrategyDetail({ params }: { params: { id: string } }) {
  const id = params.id;
  const [activeTab, setActiveTab] = useState('contract');

  // Mock data representing the detailed state of a strategy
  const strategy = {
    id: id,
    name: "Mean Reversion Nifty50",
    lifecycle_state: "BACKTESTING",
    portability: "PORTABLE",
    source: {
      type: "YouTube Transcript",
      author: "Trading Channel X",
      url: "https://youtube.com/..."
    },
    bias_warnings: [
      "Potential lookahead bias in indicator X calculation."
    ]
  };

  const tabs = [
    { id: 'source', name: 'Source & Extraction', icon: FileText },
    { id: 'contract', name: 'Signal Contract', icon: Database },
    { id: 'universe', name: 'Universe', icon: PieChart },
    { id: 'dependencies', name: 'Dependencies', icon: GitMerge },
    { id: 'research', name: 'Research Results', icon: LineChart },
    { id: 'bias', name: 'Bias & Data Quality', icon: ShieldCheck },
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 px-8 py-6">
        <div className="max-w-7xl mx-auto">
          <Link href="/" className="inline-flex items-center text-sm text-slate-500 hover:text-blue-600 mb-4">
            <ArrowLeft size={16} className="mr-1" /> Back to Dashboard
          </Link>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-3">
                {strategy.name}
                <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                  {strategy.lifecycle_state}
                </span>
              </h1>
              <p className="text-slate-500 mt-2">ID: {strategy.id} • {strategy.portability}</p>
            </div>
            <div className="flex gap-3">
              <button className="px-4 py-2 bg-white border border-slate-300 rounded-md shadow-sm font-medium hover:bg-slate-50">
                Reject Strategy
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm font-medium hover:bg-blue-700">
                Approve to Next Stage
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-8 py-8">

        {/* Alerts */}
        {strategy.bias_warnings.length > 0 && (
          <div className="mb-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg flex items-start gap-3 text-yellow-800">
            <AlertTriangle className="flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold">Bias Warning</h3>
              <p className="text-sm mt-1">{strategy.bias_warnings[0]}</p>
            </div>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-200 mb-8 overflow-x-auto">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-3 font-medium text-sm border-b-2 whitespace-nowrap ${
                  isActive
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                }`}
              >
                <Icon size={16} />
                {tab.name}
              </button>
            );
          })}
        </div>

        {/* Tab Content */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm min-h-[400px]">

          {activeTab === 'contract' && (
            <div>
              <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <Database className="text-slate-400" /> Deterministic Signal Contract
              </h2>
              <div className="bg-slate-900 rounded-lg p-4 font-mono text-sm text-green-400 overflow-x-auto">
                <pre>{`{
  "operator": "AND",
  "conditions": [
    {
      "left": "close",
      "operator": ">",
      "right": "sma(close, 200)"
    },
    {
      "left": "rsi(close, 14)",
      "operator": "<",
      "right": 35
    }
  ],
  "exit_rule": "rsi(close, 14) > 70",
  "stop_loss_pct": 2.5
}`}</pre>
              </div>
              <div className="mt-6 grid grid-cols-2 gap-4">
                 <div className="border border-slate-200 rounded-lg p-4">
                    <h3 className="font-semibold text-slate-700 text-sm">Timeframe</h3>
                    <p className="mt-1 text-lg">1 Day</p>
                 </div>
                 <div className="border border-slate-200 rounded-lg p-4">
                    <h3 className="font-semibold text-slate-700 text-sm">Evaluation Frequency</h3>
                    <p className="mt-1 text-lg">End of Day</p>
                 </div>
              </div>
            </div>
          )}

          {activeTab === 'source' && (
            <div>
               <h2 className="text-xl font-semibold mb-4">Source & Extraction</h2>
               <div className="space-y-4">
                  <div className="p-4 border border-slate-200 rounded-lg bg-slate-50">
                    <p className="text-sm text-slate-500 font-medium">Original Source Type</p>
                    <p className="font-medium mt-1">{strategy.source.type}</p>
                  </div>
                  <div className="p-4 border border-slate-200 rounded-lg bg-slate-50">
                    <p className="text-sm text-slate-500 font-medium">Author/Channel</p>
                    <p className="font-medium mt-1">{strategy.source.author}</p>
                  </div>
               </div>
            </div>
          )}

          {/* Placeholder for other tabs */}
          {['universe', 'dependencies', 'research', 'bias'].includes(activeTab) && (
            <div className="flex flex-col items-center justify-center h-64 text-slate-400">
               <p>Content for {tabs.find(t => t.id === activeTab)?.name} goes here.</p>
               <p className="text-sm mt-2">Connecting to backend services...</p>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}
