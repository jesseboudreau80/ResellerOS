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
}
