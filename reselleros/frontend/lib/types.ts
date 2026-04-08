export interface Item {
  sku: string;
  title: string;
  description: string;
  price: number;
  cost: number;
  profit: number;
  barcode: string;
  barcode_type: 'UPC' | 'EAN' | 'CODE128' | string;
  shelf_location: string | null;
  status: 'available' | 'listed' | 'pending' | 'sold' | string;
  date_added: string;
}

export interface DashboardStats {
  total_inventory: number;
  items_listed: number;
  items_sold: number;
  inventory_value: number;
  profit: number;
  auctions_currently_watching: number;
  auctions_won_this_month: number;
  average_roi: number;
  best_performing_facility: string;
}

export interface Auction {
  id: number;
  platform: string;
  facility_name: string;
  city: string | null;
  unit_id: string;
  unit_size: string | null;
  bid_status: string;
  current_bid: number;
  max_bid: number;
  did_win: boolean;
  total_revenue: number;
  total_cost: number;
  roi_percent: number;
  locker_type: string | null;
}
