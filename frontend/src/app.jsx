import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  DollarSign, 
  PieChart, 
  Target, 
  ShieldCheck, 
  Activity, 
  PlusCircle, 
  ArrowUpRight, 
  ArrowDownRight,
  Wallet,
  Calendar,
  Layers,
  RefreshCw
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [backendStatus, setBackendStatus] = useState('checking');
  const [transactions, setTransactions] = useState([
    { id: 1, title: 'Salary Deposit', category: 'Income', amount: 4500, type: 'income', date: '2026-09-01' },
    { id: 2, title: 'Grocery Shopping', category: 'Food', amount: 142.50, type: 'expense', date: '2026-09-03' },
    { id: 3, title: 'Cloud Server Subscription', category: 'Services', amount: 35.00, type: 'expense', date: '2026-09-04' },
    { id: 4, title: 'Stock Dividend', category: 'Investments', amount: 120.00, type: 'income', date: '2026-09-05' },
    { id: 5, title: 'Electric Utility Bill', category: 'Utilities', amount: 89.20, type: 'expense', date: '2026-09-06' },
  ]);

  const [budgets, setBudgets] = useState([
    { id: 1, category: 'Housing & Utilities', allocated: 1500, spent: 1100, color: 'bg-emerald-500' },
    { id: 2, category: 'Food & Dining', allocated: 600, spent: 480, color: 'bg-blue-500' },
    { id: 3, category: 'Entertainment & Tech', allocated: 300, spent: 260, color: 'bg-indigo-500' },
    { id: 4, category: 'Transportation', allocated: 400, spent: 180, color: 'bg-cyan-500' },
  ]);

  const [goals, setGoals] = useState([
    { id: 1, name: 'Emergency Fund', target: 10000, current: 7500, deadline: 'Dec 2026' },
    { id: 2, name: 'Investment Portfolio', target: 25000, current: 14200, deadline: 'Jun 2027' },
    { id: 3, name: 'Vacation Savings', target: 3000, current: 2400, deadline: 'Nov 2026' },
  ]);

  const [newTx, setNewTx] = useState({ title: '', category: 'Food', amount: '', type: 'expense' });

  const checkBackend = async () => {
    setBackendStatus('checking');
    try {
      const res = await fetch('/api/v1/health');
      if (res.ok) {
        const data = await res.json();
        setBackendStatus(data.status === 'healthy' ? 'online' : 'error');
      } else {
        setBackendStatus('offline');
      }
    } catch {
      setBackendStatus('offline');
    }
  };

  useEffect(() => {
    checkBackend();
  }, []);

  const totalIncome = transactions.filter(t => t.type === 'income').reduce((acc, t) => acc + Number(t.amount), 0);
  const totalExpense = transactions.filter(t => t.type === 'expense').reduce((acc, t) => acc + Number(t.amount), 0);
  const netSavings = totalIncome - totalExpense;

  const handleAddTransaction = (e) => {
    e.preventDefault();
    if (!newTx.title || !newTx.amount) return;
    const item = {
      id: Date.now(),
      title: newTx.title,
      category: newTx.category,
      amount: parseFloat(newTx.amount),
      type: newTx.type,
      date: new Date().toISOString().split('T')[0]
    };
    setTransactions([item, ...transactions]);
    setNewTx({ title: '', category: 'Food', amount: '', type: 'expense' });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navigation */}
      <header className="border-b border-slate-800 bg-slate-900/70 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-tr from-emerald-500 to-teal-400 rounded-xl text-slate-950 shadow-lg shadow-emerald-500/20">
              <ShieldCheck className="w-6 h-6 stroke-[2.5]" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                Fortify Finance
              </span>
            </div>
          </div>

          {/* Backend Status Indicator */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-full border border-slate-700/60 text-xs">
              <span className={`w-2.5 h-2.5 rounded-full ${
                backendStatus === 'online' ? 'bg-emerald-400 animate-pulse' :
                backendStatus === 'checking' ? 'bg-amber-400' : 'bg-rose-500'
              }`} />
              <span className="text-slate-300 font-medium">
                Backend API: {backendStatus === 'online' ? 'Connected (Port 8000)' : backendStatus === 'checking' ? 'Checking...' : 'Disconnected'}
              </span>
              <button onClick={checkBackend} title="Refresh connection" className="text-slate-400 hover:text-white transition">
                <RefreshCw className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="w-8 h-8 rounded-full bg-emerald-600/30 border border-emerald-500/40 flex items-center justify-center font-semibold text-emerald-400 text-sm">
              Z
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Layout */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        {/* Navigation Tabs */}
        <div className="flex space-x-2 border-b border-slate-800 pb-4 mb-8">
          {[
            { id: 'dashboard', label: 'Dashboard', icon: Activity },
            { id: 'transactions', label: 'Transactions', icon: DollarSign },
            { id: 'budgets', label: 'Budgets', icon: PieChart },
            { id: 'goals', label: 'Savings Goals', icon: Target },
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  active
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Overview Stats Bar */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-sm relative overflow-hidden">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-400">Total Income</span>
              <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-400">
                <ArrowUpRight className="w-5 h-5" />
              </div>
            </div>
            <div className="text-2xl font-bold text-white">${totalIncome.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
            <div className="text-xs text-emerald-400 mt-2 font-medium flex items-center space-x-1">
              <span>+12% from last month</span>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-sm relative overflow-hidden">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-400">Total Expenses</span>
              <div className="p-2 bg-rose-500/10 rounded-lg text-rose-400">
                <ArrowDownRight className="w-5 h-5" />
              </div>
            </div>
            <div className="text-2xl font-bold text-white">${totalExpense.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
            <div className="text-xs text-slate-400 mt-2 font-medium flex items-center space-x-1">
              <span>Within planned monthly budget</span>
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 shadow-sm relative overflow-hidden">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-400">Net Balance</span>
              <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-400">
                <Wallet className="w-5 h-5" />
              </div>
            </div>
            <div className="text-2xl font-bold text-emerald-400">${netSavings.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
            <div className="text-xs text-emerald-400/80 mt-2 font-medium flex items-center space-x-1">
              <span>Healthy positive cash flow</span>
            </div>
          </div>
        </div>

        {/* Tab Views */}
        {activeTab === 'dashboard' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Quick Transaction Add */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 lg:col-span-1">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
                <PlusCircle className="w-5 h-5 text-emerald-400" />
                <span>Quick Add Transaction</span>
              </h3>
              <form onSubmit={handleAddTransaction} className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Description</label>
                  <input
                    type="text"
                    value={newTx.title}
                    onChange={(e) => setNewTx({ ...newTx, title: e.target.value })}
                    placeholder="e.g., Grocery, Rent, Coffee"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
                    required
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-400 mb-1">Amount ($)</label>
                    <input
                      type="number"
                      step="0.01"
                      value={newTx.amount}
                      onChange={(e) => setNewTx({ ...newTx, amount: e.target.value })}
                      placeholder="0.00"
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-400 mb-1">Type</label>
                    <select
                      value={newTx.type}
                      onChange={(e) => setNewTx({ ...newTx, type: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
                    >
                      <option value="expense">Expense</option>
                      <option value="income">Income</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Category</label>
                  <select
                    value={newTx.category}
                    onChange={(e) => setNewTx({ ...newTx, category: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500"
                  >
                    <option value="Food">Food & Dining</option>
                    <option value="Housing">Housing & Rent</option>
                    <option value="Utilities">Utilities</option>
                    <option value="Transportation">Transportation</option>
                    <option value="Investments">Investments</option>
                    <option value="Income">Salary / Income</option>
                    <option value="Services">Services & Subscriptions</option>
                  </select>
                </div>
                <button
                  type="submit"
                  className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold rounded-lg text-sm transition-all shadow-lg shadow-emerald-500/20"
                >
                  Record Entry
                </button>
              </form>
            </div>

            {/* Recent Activity */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 lg:col-span-2">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Recent Transactions</h3>
                <button onClick={() => setActiveTab('transactions')} className="text-xs text-emerald-400 hover:underline">
                  View All
                </button>
              </div>
              <div className="divide-y divide-slate-800">
                {transactions.slice(0, 5).map((t) => (
                  <div key={t.id} className="py-3.5 flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg ${t.type === 'income' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-800 text-slate-300'}`}>
                        {t.type === 'income' ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-white">{t.title}</div>
                        <div className="text-xs text-slate-400">{t.category} • {t.date}</div>
                      </div>
                    </div>
                    <div className={`text-sm font-semibold ${t.type === 'income' ? 'text-emerald-400' : 'text-slate-200'}`}>
                      {t.type === 'income' ? '+' : '-'}${Number(t.amount).toFixed(2)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'transactions' && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Transaction History</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 text-xs uppercase tracking-wider">
                    <th className="pb-3 font-semibold">Description</th>
                    <th className="pb-3 font-semibold">Category</th>
                    <th className="pb-3 font-semibold">Date</th>
                    <th className="pb-3 font-semibold text-right">Amount</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {transactions.map((t) => (
                    <tr key={t.id} className="hover:bg-slate-800/30 transition">
                      <td className="py-4 font-medium text-white">{t.title}</td>
                      <td className="py-4 text-slate-400">{t.category}</td>
                      <td className="py-4 text-slate-400">{t.date}</td>
                      <td className={`py-4 text-right font-semibold ${t.type === 'income' ? 'text-emerald-400' : 'text-slate-200'}`}>
                        {t.type === 'income' ? '+' : '-'}${Number(t.amount).toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'budgets' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {budgets.map((b) => {
              const percentage = Math.min(100, Math.round((b.spent / b.allocated) * 100));
              return (
                <div key={b.id} className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
                  <div className="flex justify-between items-center mb-3">
                    <h4 className="font-semibold text-white">{b.category}</h4>
                    <span className="text-xs text-slate-400">${b.spent} of ${b.allocated}</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-3 overflow-hidden">
                    <div className={`h-full rounded-full ${b.color}`} style={{ width: `${percentage}%` }} />
                  </div>
                  <div className="flex justify-between items-center mt-3 text-xs text-slate-400">
                    <span>{percentage}% used</span>
                    <span>${b.allocated - b.spent} remaining</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {activeTab === 'goals' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {goals.map((g) => {
              const progress = Math.min(100, Math.round((g.current / g.target) * 100));
              return (
                <div key={g.id} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-semibold text-white">{g.name}</h4>
                      <Target className="w-5 h-5 text-emerald-400" />
                    </div>
                    <div className="text-2xl font-bold text-white mb-4">
                      ${g.current.toLocaleString()} <span className="text-xs font-normal text-slate-400">/ ${g.target.toLocaleString()}</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden mb-2">
                      <div className="bg-emerald-400 h-full rounded-full" style={{ width: `${progress}%` }} />
                    </div>
                  </div>
                  <div className="flex justify-between items-center text-xs text-slate-400 mt-4 pt-3 border-t border-slate-800">
                    <span>Progress: {progress}%</span>
                    <span>Target: {g.deadline}</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}