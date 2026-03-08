import { DashboardStats, Item } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error(`API error ${response.status}`);
  }

  return response.json();
}

export const api = {
  getDashboard: () => request<DashboardStats>('/dashboard'),
  getItems: () => request<Item[]>('/items'),
  createItem: (payload: { title: string; cost: number; price: number; shelf_location: string }) =>
    request<Item>('/items/create', { method: 'POST', body: JSON.stringify(payload) }),
  markSold: (sku: string) => request(`/items/${sku}/mark_sold`, { method: 'POST' }),
  deleteItem: (sku: string) => request(`/items/${sku}`, { method: 'DELETE' }),
  updateItem: (sku: string, payload: Partial<Item>) =>
    request<Item>(`/items/${sku}`, { method: 'PUT', body: JSON.stringify(payload) }),
};
