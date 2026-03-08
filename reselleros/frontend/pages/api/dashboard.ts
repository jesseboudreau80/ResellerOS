import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const response = await fetch(`${backendUrl}/dashboard`);
    
    if (!response.ok) {
      return res.status(response.status).json({ 
        error: `Backend returned ${response.status}` 
      });
    }
    
    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('Dashboard API error:', error);
    res.status(500).json({ 
      error: 'Failed to fetch dashboard data',
      details: error instanceof Error ? error.message : String(error)
    });
  }
}
